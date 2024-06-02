from datetime import datetime


def title_scraper(soup):
    title = soup.find('title')
    if title:
        return title.text.strip()

    title_meta = soup.find('meta', property='og:title') or soup.find('meta', name='twitter:title')
    if title_meta:
        return title_meta['content'].strip()

    for header_tag in soup.find('h1'):
        if header_tag.text.strip():
            return header_tag.text.strip()

    for header2_tag in soup.find('h2'):
        if header2_tag.text.strip():
            return header2_tag.text.strip()

    return "No title"


def main_text_scraper(soup):
    main_content = soup.find('div', class_='article-content') or soup.find(id='main-content')
    if main_content:
        return main_content.get_text(separator='\n').strip()

    article_tag = soup.find('article')
    if article_tag:
        return article_tag.get_text(separator='\n').strip()

    return "No main text"


def img_path_scraper(soup):
    img_meta = soup.find('meta', property='og:image') or soup.find('meta', name='twitter:image')
    if img_meta and img_meta.has_attr('content'):
        return img_meta['content'].strip()

    main_image = soup.find(class_='main-image') or soup.find('img', class_='main-img') or soup.find('img',
                                                                                                    class_='header-image')
    if main_image and main_image.has_attr('src'):
        return main_image['src'].strip()

    img_meta = soup.find('meta', property='og:image') or soup.find('meta', name='twitter:image')
    if img_meta and img_meta.has_attr('content'):
        return img_meta['content'].strip()

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
            return f"Error with date parsing: {date_str}"
    else:
        return "No date found"

