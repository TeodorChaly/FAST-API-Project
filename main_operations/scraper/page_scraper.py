from datetime import datetime
from bs4 import Comment


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

        for tag, attrs in candidates:
            main_content = soup.find(tag, **attrs)
            if main_content and len(main_content.get_text(separator='\n').strip()) > 100:
                return clean_text(main_content.get_text(separator='\n').strip())

        other_divs = soup.find_all('div', class_='content')
        for div in other_divs:
            if len(div.get_text(separator='\n').strip()) > 100:
                return clean_text(div.get_text(separator='\n').strip())

        paragraphs = soup.find_all('p')
        combined_text = '\n'.join(
            p.get_text(separator='\n').strip() for p in paragraphs if len(p.get_text().strip()) > 50)
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
        img_meta = soup.find('meta', attrs={'property': 'og:image'}) or soup.find('meta',
                                                                                  attrs={'property': 'og:image'})
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
