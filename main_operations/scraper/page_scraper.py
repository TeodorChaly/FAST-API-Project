from urllib.parse import urljoin
from datetime import datetime
from bs4 import BeautifulSoup
from bs4 import Comment
import trafilatura
import requests


def extract_images_from_main_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_content = (soup.find('main') or
                    soup.find('article') or
                    soup.find('div', class_='content') or
                    soup.find('div', class_='post-content') or
                    soup.find('section', class_='main-content') or
                    soup.body)

    if not main_content:
        return []

    images = main_content.find_all('img')
    image_info = []

    min_width = 700
    min_height = 300
    for img in images:
        img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
        if img_url:
            full_img_url = urljoin(url, img_url)

            img_alt = img.get('alt') or "No alt text"

            width = img.get('width')
            height = img.get('height')
            if width and height:
                try:
                    width_value = int(width.replace('px', '').strip())
                    height_value = int(height.replace('px', '').strip())
                except ValueError:
                    continue

                if width_value >= min_width and height_value >= min_height and img_alt != "No alt text":
                    image_info.append({
                        'url': full_img_url,
                        'alt': img_alt,
                        'width': width,
                        'height': height
                    })

    image_info = sorted(image_info, key=lambda x: (x['alt'] != "No alt text"), reverse=True)

    return image_info


# url = 'https://andybradford.dev/2021/08/31/detailed-vw-golf-8-review-have-you-tried-turning-it-off-and-on-again/'
#
# images = extract_images_from_main_content(url)
# for img in images:
#     print(f"Image URL: {img['url']}")
#     print(f"Alt text: {img['alt']}")
#     print(f"Width: {img['width']}, Height: {img['height']}")
#     print("-" * 30)


def title_scraper(soup):
    title = soup.find('title')
    if title:
        return title.text.strip()

    title_meta = soup.find('meta', property='og:title') or soup.find('meta', name='twitter:title')
    if title_meta:
        return title_meta['content'].strip()

    header_tag = soup.find('h1')
    if header_tag:
        return header_tag.text.strip()

    header2_tag = soup.find('h2')
    if header2_tag:
        return header2_tag.text.strip()

    return "No title"


def h1_scraper(soup):
    header_tag = soup.find('h1')
    if header_tag:
        return header_tag.text.strip()

    header2_tag = soup.find('h2')
    if header2_tag:
        return header2_tag.text.strip()

    return "No title"


def additional_info_scraper(soup):
    candidates = [
        ('div', {'class': 'article-content'}),
        ('div', {'id': 'main-content'}),
        ('div', {'class': 'main-content'}),
        ('div', {'id': 'article-content'}),
        ('article', {}),
        ('section', {'class': 'main-section'}),
        ('main', {}),
    ]

    images = []
    for tag, attrs in candidates:
        main_content = soup.find(tag, **attrs)
        if main_content:
            imgs = main_content.find_all('img', recursive=True)
            images.extend(imgs)

    image_info = [
        f"[Image: {img.get('src')}, alt: {img.get('alt', '')}]" for img in images if img.get('src')
    ]
    return '\n'.join(image_info)


def main_content_download(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text


def extract_links_and_text(soup):
    results = []

    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)
        if href:
            results.append({
                'link': href,
                'text': text if text else None
            })
    return results


def add_links_to_text(main_text, soup):
    for i in extract_links_and_text(soup):
        if i["text"] is not None:
            if i["text"] in main_text:

                if "http" in i["link"] or "https" in i["link"]:
                    main_text = main_text.replace(i["text"], str(i["text"] + ", " + i["link"]), 1)
    return main_text


def main_text_scraper(soup):
    try:
        for element in soup(["script", "style"]):
            element.decompose()

        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        candidates = [
            ('div', {'class': 'article-content'}),
            ('div', {'id': 'main-content'}),
            ('div', {'class': 'main-content'}),
            ('div', {'id': 'article-content'}),
            ('article', {}),
            ('section', {'class': 'main-section'}),
            ('main', {}),
        ]

        elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'],
                                 recursive=True)  # , 'li', 'blockquote'
        combined_text = '\n'.join(
            el.get_text(separator='\n').strip()
            for el in elements if len(el.get_text().strip()) > 50 or el.name.startswith('h')
        )

        if combined_text.strip():
            return clean_text(combined_text.strip())

        for tag, attrs in candidates:
            main_content = soup.find(tag, **attrs)

            if main_content and len(main_content.get_text(separator='\n').strip()) > 100:
                raw_text = main_content.get_text(separator='\n').strip()
                return clean_text(raw_text)

        other_divs = soup.find_all('div', class_='content')
        for div in other_divs:
            if len(div.get_text(separator='\n').strip()) > 100:
                return clean_text(div.get_text(separator='\n').strip())

        return "No main text found"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Error"


def structure_text_scraper(soup):
    try:
        for element in soup(["script", "style"]):
            element.decompose()

        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        candidates = [
            ('div', {'class': 'article-content'}),
            ('div', {'id': 'main-content'}),
            ('div', {'class': 'main-content'}),
            ('div', {'id': 'article-content'}),
            ('article', {}),
            ('section', {'class': 'main-section'}),
            ('main', {}),
        ]

        main_content = None
        for tag, attrs in candidates:
            main_content = soup.find(tag, attrs)
            if main_content:
                break

        if not main_content:
            main_content = soup.find('body')

        for element in main_content.find_all(['nav', 'footer', 'aside', 'header']):
            element.decompose()

        elements = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'li', 'blockquote'],
                                         recursive=True)
        combined_text = ''

        for el in elements:
            text_parts = []

            if el.name == 'img':
                src = el.get('src', '').strip()
                alt = el.get('alt', '').strip()
                if src:
                    img_info = f'<img src="{src}" alt="{alt}">' if alt else f'<img src="{src}">'
                    text_parts.append(img_info)
            elif el.name == 'li':
                li_text = el.get_text().strip()
                text_parts.append(li_text)
            else:
                for child in el.children:
                    if child.name == 'a' and 'href' in child.attrs:
                        link_text = child.get_text().strip()

                        href = child['href']
                        text_parts.append(f'<a href="{href}">{link_text}</a>')
                    elif isinstance(child, str):
                        text_parts.append(child.strip())

            text = ' '.join(text_parts).strip()
            if len(text) > 50 or el.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote']:
                combined_text += f'<{el.name}>{text}</{el.name}>\n'

        if combined_text.strip():
            return clean_text(combined_text.strip())

        return "No main text found"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Error"


def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if len(line) > 10 and not any(
                phrase in line.lower() for phrase in [
                    'ask questions', 'find answers', 'collaborate', 'subscribe', 'rss feed',
                    'learn more', 'post your answer', 'terms of service', 'privacy policy',
                    'site design', 'logo', 'stack exchange', 'licensed under'
                ]
        ):
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def img_path_scraper(soup):
    try:
        img_meta = soup.find('meta', attrs={'property': 'og:image'})
        if img_meta and img_meta.has_attr('content'):
            return img_meta['content'].strip()

        main_image = soup.find('img', class_='main-image') or soup.find('img', class_='main-img') or soup.find('img',
                                                                                                               class_='header-image')
        if main_image and main_image.has_attr('src'):
            return main_image['src'].strip()

        return "Image not found"
    except Exception as e:
        print("Error during scrapping img", e)
        return "Image not found"


def date_published_scraper(soup):
    date_meta = soup.find('meta', property='article:published_time')
    if date_meta and date_meta.has_attr('content'):
        return date_meta['content'].strip()

    date_class = soup.find(class_='publish-date')
    if date_class and date_class.has_attr('datetime'):
        return date_class['datetime'].strip()

    date_tags = soup.find_all(['time', 'span'], class_=lambda x: x and 'date' in x)
    for tag in date_tags:
        if tag.has_attr('datetime'):
            return tag['datetime'].strip()
        if tag.has_attr('content'):
            return tag['content'].strip()
        if tag.has_attr('title'):
            return tag['title'].strip()
        if tag.has_attr('aria-label'):
            return tag['aria-label'].strip()
        if tag.string:
            return tag.string.strip()

    time_tag = soup.find('time')
    if time_tag:
        date_str = time_tag.text.strip()
        try:
            date_time = datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')
            return date_time.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return "No date found"
    else:
        return "No date found"
