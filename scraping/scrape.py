from bs4 import BeautifulSoup
from request_via_cloudscraper import request_via_cloudscraper
import re
from database import add_to_diary_entries_table, insert_tag, get_diary_entry_id, insert_diary_entry_tag, create_diary_entries_table, create_tags_table, create_diary_entry_tags_table
import datetime

letterboxd_url = "https://letterboxd.com/"
username= "28_joes_later"
diary_url = "/diary/films/page/"
review_url = "/reviews/films/page/1/"
tags_url = "/tags/films/"

def star_converter(stars):
    match stars:
        case "½":
            return 1
        case "★":
            return 2
        case "★½":
            return 3
        case "★★":
            return 4
        case "★★½":
            return 5
        case "★★★":
            return 6
        case "★★★½":
            return 7
        case "★★★★":
            return 8
        case "★★★★½":
            return 9
        case "★★★★★":
            return 10

def liked_converter(liked_string):
    if liked_string == "Liked":
        return True
    else:
        return False

def scrape_diary(diary_html):
    soup = BeautifulSoup(diary_html, "html.parser")
    diary_entries = soup.find_all("tr", class_=re.compile("diary-entry-row viewing-poster-container"))
    reviews = []
    for diary_entry in diary_entries:
        # Extract date reviewed (month and day)
        month_elem = diary_entry.find("a", class_="month")
        day_elem = diary_entry.find("a", class_="daydate")
        year_elem = diary_entry.find("a", class_="year")
        
        date_watched = None
        if month_elem and day_elem and year_elem:
            month = month_elem.text.strip()
            day = day_elem.text.strip()
            year = year_elem.text.strip()
            date_watched = f"{day} {month} {year}"
        elif day_elem:
            # If month is not available, try to extract from the daydate href
            # Format: /28_joes_later/diary/films/for/YYYY/MM/DD/
            day_href = day_elem.get("href", "")
            parts = day_href.strip("/").split("/")
            if len(parts) >= 6:
                try:
                    year = parts[-3]
                    month_num = parts[-2]
                    day = day_elem.text.strip()
                    # Convert month number to month name
                    import calendar
                    month = calendar.month_abbr[int(month_num)]
                    date_watched = f"{day} {month} {year}"
                except (ValueError, IndexError):
                    date_watched = None

        date_watched = datetime.datetime.strptime(date_watched, "%d %b %Y").strftime("%Y-%m-%d")

        
        # Extract film title from h2 > a
        film_title_elem = diary_entry.find("h2", class_="name")
        if not film_title_elem:
            film_title_elem = diary_entry.find("h2", class_="primaryname")
        
        if film_title_elem:
            title_link = film_title_elem.find("a")
            if title_link:
                film_title = title_link.text.strip()
            else:
                film_title = None
        else:
            film_title = None
        
        # Extract film year
        year_span = diary_entry.find("span", class_="releasedate")
        if year_span:
            film_year = year_span.text.strip()
        else:
            film_year = None
        
        # Extract star rating
        rating_elem = diary_entry.find("span", class_=re.compile("rating rated-"))
        if rating_elem:
            rating_text = rating_elem.text.strip()
            rating = star_converter(rating_text)
        else:
            rating = None
        
        # Check if liked
        like_col = diary_entry.find("td", class_="col-like")
        liked = False
        if like_col and like_col.find("span", class_="icon-liked"):
            liked = True
        
        reviews.append({
            "film_title": film_title,
            "film_year": film_year,
            "rating": rating,
            "liked": liked,
            "date_watched": date_watched
        })
    
    return reviews

def get_page_count(diary_html):
    soup = BeautifulSoup(diary_html, "html.parser")
    pagination = soup.find("div", class_="pagination")
    if not pagination:
        return 1

    page_numbers = set()

    # numeric links in page list
    for a in pagination.find_all("a", href=True):
        text = a.text.strip()
        if text.isdigit():
            page_numbers.add(int(text))

    if not page_numbers:
        return 1

    return max(page_numbers)


def scrape_reviews(review_html):
    soup = BeautifulSoup(review_html, "html.parser")
    review_soup = soup.find_all("div", class_=re.compile("listitem js-listitem"))
    reviews = []
    for review_entry in review_soup:
        review_body = (review_entry.text).split("  ")
        review_body = list(filter(None, review_body))
        review_body = [i.strip() for i in review_body]
        film_title = review_body[0][:-5]
        film_year = review_body[0][-4:]
        rating = star_converter(review_body[1])
        liked = liked_converter(review_body[2])
        if liked:
            date_watched = review_body[4]
            film_review = review_body[5]
        else: 
            date_watched = review_body[3]
            film_review = review_body[4]

        date_watched = datetime.datetime.strptime(date_watched[:11], "%d %b %Y").strftime("%Y-%m-%d")

        reviews.append({"film_title": film_title, "film_year": film_year, "rating": rating, "liked": liked, "date_watched": date_watched, "film_review": film_review})

    return reviews

def scrape_tags(tags_url):
    """Parse a Letterboxd tags page HTML and return a list of tag strings.

    Accepts either an HTML string or bytes and returns the visible tag text
    for links like `/username/tag/<tag>/films/` in document order.
    """
    tags_html = tags_url
    if not tags_html:
        return []
    if isinstance(tags_html, bytes):
        tags_html = tags_html.decode("utf-8", errors="ignore")

    soup = BeautifulSoup(tags_html, "html.parser")

    # Find anchors linking to tags (pattern: /<user>/tag/<tag>/films/)
    tag_links = soup.find_all("a", href=re.compile(r"/[^/]+/tag/.+?/films/"))

    tags = []
    for a in tag_links:
        href = a.get('href')
        if not href:
            continue
        # Make absolute
        if href.startswith('/'):
            href = letterboxd_url.rstrip('/') + href
        # Replace trailing '/films/' with '/diary/'
        href = re.sub(r'/films/?$', '/diary/', href)
        tags.append(href)

    # Deduplicate while preserving order
    seen = set()
    tag_url_list = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            tag_url_list.append(t)

    # Extract tag names from URLs
    tag_list = []
    for url in tag_url_list:
        parts = url.split('tag/')
        if len(parts) > 1:
            tag_part = parts[1].split('/diary/')[0]
            tag_list.append(tag_part)

    return tag_list, tag_url_list



if __name__ == '__main__':
    diary_pages_html = []
    i = 1
    max_page_number = 10000
    while i <= max_page_number:
        diary_html = request_via_cloudscraper(letterboxd_url + username + diary_url + str(i) + "/", file = f"html_store//diary_{i}", test=True)
        if i == 1:
            max_page_number = get_page_count(diary_html)
        diary_pages_html.append(diary_html)
        if not diary_html:
            break
        i += 1

    create_diary_entries_table()
    create_tags_table()
    create_diary_entry_tags_table()
    all_diary_entries = []
    for diary_html in diary_pages_html:
        diary_entries = scrape_diary(diary_html)
        all_diary_entries.extend(diary_entries)

    add_to_diary_entries_table(all_diary_entries)

    tags_html = request_via_cloudscraper(letterboxd_url + username + tags_url, file="tags", test=True)
    tag_list, tag_url_list = scrape_tags(tags_html)
    for tag, tag_url in zip(tag_list, tag_url_list):
        tag_pages_html = []
        j = 1
        max_tag_page_number = 10000
        while j <= max_tag_page_number:
            tag_diary_html = request_via_cloudscraper(tag_url + f"/page/{j}/", file=f"html_store//tag_diary_{tag}_{j}", test=True)
            if j == 1:
                max_tag_page_number = get_page_count(tag_diary_html)
            tag_pages_html.append(tag_diary_html)
            if not tag_diary_html:
                break
            j += 1

        tag_id = insert_tag(tag)
        all_tag_diary_entries = []
        for tag_diary_html in tag_pages_html:
            tag_diary_entries = scrape_diary(tag_diary_html)
            all_tag_diary_entries.extend(tag_diary_entries)

        for entry in all_tag_diary_entries:
            diary_entry_id = get_diary_entry_id(entry['film_title'], entry['film_year'], entry['date_watched'])
            if diary_entry_id:
                insert_diary_entry_tag(diary_entry_id, tag_id)

# Got list of tags, now need to get diary entries for each tag and add to database.