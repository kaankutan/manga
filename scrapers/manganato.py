from slugify import slugify
import requests
from bs4 import BeautifulSoup
import logging
import boto3
from io import BytesIO
from datetime import datetime
from index.models import Slider, Chapter, Manga

session = boto3.session.Session(
    aws_access_key_id="AKIAW4O3BS6BRY53X7FR",
    aws_secret_access_key="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",
    region_name="eu-central-1"
)
s3_client = session.client('s3')


def get_manga_urls(page):
    r = requests.get(f"https://manganato.com/advanced_search?s=all&orby=topview&page={page}")
    soup = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
    return [div.find("a").get("href") for div in soup.find_all(attrs={"class": "content-genres-item"})]


def get_manga(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
        title = soup.find("h1").text
        slug = slugify(title)
        thumbnail = soup.find(attrs={"property": "og:image"}).get("content")
        description = soup.find(attrs={"id": "panel-story-info-description"}).text.replace("Description :", "").split()
        description = " ".join(description)
        categories = [
            a.text
            for tr in soup.find(attrs={"class": "variations-tableInfo"}).find_all("tr")
            if "Genres" in str(tr)
            for a in tr.find(attrs={"class": "table-value"}).find_all("a")
        ]

        if not manga.count_documents({"slug": slug}):
            r = requests.get(thumbnail)
            image_url = f"en/manga_thumbnail/{slug}.jpg"
            data = BytesIO(bytes(r.content))
            s3_client.upload_fileobj(
                data, "hoshiko-cdn", image_url,
                ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}
            )
            _id = manga.insert_one({
                "title": title,
                "slug": slug,
                "view": 0,
                "description": description,
                "thumbnail": f"/{image_url}",
                "categories": categories,
                "created_at": datetime.now()
            }).inserted_id
        else:
            _id = manga.find_one({"slug": slug})['_id']
        chapters_list = [
            {"url": chapter.get("href"), "name": chapter.text}
            for chapter in soup.find(attrs={"class": "panel-story-chapter-list"}).find_all("a")
        ]
        chapters_list.reverse()
        for chapter in chapters_list:
            chapter_slug = slugify(chapter['name'])
            if not chapters.count_documents({"slug": chapter_slug, "manga_id": _id}):
                try:
                    chapter_pages = []
                    r = requests.get(chapter['url'])
                    soup = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
                    pages = [img.get("src") for img in soup.find(attrs={"class": "container-chapter-reader"}).find_all("img")]
                    i = 0
                    for page in pages:
                        i += 1
                        r = requests.get(page, headers={"referer": "https://readmanganato.com/"})
                        image_url = f"en/manga_chapters/{slug}/{chapter_slug}/{i}.jpg"
                        data = BytesIO(bytes(r.content))
                        s3_client.upload_fileobj(
                            data, "hoshiko-cdn", image_url,
                            ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}
                        )
                        chapter_pages.append(f"/{image_url}")
                    chapters.insert_one({
                        "manga_id": _id,
                        "name": chapter['name'],
                        "slug": chapter_slug,
                        "pages": chapter_pages,
                        "created_at": datetime.now()
                    })
                except requests.exceptions.RequestException:
                    pass
    except Exception as e:
        logging.error(e)
