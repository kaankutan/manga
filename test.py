import os

import django
import pymongo
from io import BytesIO
import requests
from mal import Manga as malManga
import boto3
from django.utils.timezone import make_aware

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'manga.settings'
)
django.setup()

from index.models import Slider, Chapter, Manga

session = boto3.session.Session(
    aws_access_key_id="AKIAW4O3BS6BRY53X7FR",
    aws_secret_access_key="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",
    region_name="eu-central-1"
)
s3_client = session.client('s3')

MONGODB_URI = "mongodb+srv://admin:ebcCOFpzRv649Gr9@hoshiko-db.dd9mj.mongodb.net"
# git clone https://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@github.com/kaankutan/manga.git
# client = pymongo.MongoClient(MONGODB_URI)

if __name__ == "__main__":
    print(Manga.objects.distinct('language').values('language'))
    # for manga_obj in Manga.objects.all():
    #     r = requests.get(
    #         "https://myanimelist.net/search/prefix.json",
    #         params={"type": "manga", "keyword": manga_obj.title, "v": "1"}
    #     )
    #     manga_search = r.json()['categories'][0]['items'][0]
    #     if 1.5 < manga_search['es_score']:
    #         mal_manga = malManga(manga_search['id'])
    #         # r = requests.get(mal_manga.image_url.replace(".jpg", "l.jpg"))
    #         # data = BytesIO(bytes(r.content))
    #         # s3_client.upload_fileobj(
    #         #     data, "hoshiko-cdn", f"en/manga_thumbnail/{manga_obj.slug}.jpg",
    #         #     ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}
    #         # )
    #         manga_obj.title = mal_manga.title
    #         manga_obj.description = mal_manga.synopsis.split("  ")[0]
    #         manga_obj.save()
    #         print(manga_obj.title, "Saved", manga_search['es_score'], sep="|")
    #     else:
    #         print(manga_obj.title, "Not saved", manga_search['es_score'], sep="|")
    # Slider(
    #     title="Kimetsu No Yaiba",
    #     description="Tanjiro is the oldest son in his family who has lost his father. One day, Tanjiro ventures off to another town to sell charcoal. Instead of going home, he ends up staying the night at someone else's house due to rumors of a demon nearby in the mountains. When he gets home the following day, a terrible tragedy awaits him.",
    #     thumbnail="/en/slider/kimetsu-no-yaiba.jpg",
    #     url="/en/manga/kimetsu-no-yaiba",
    #     language="en"
    # ).save()
    #
    # Slider(
    #     title="Solo Leveling",
    #     description="Hunters, humans who possess magical abilities, must battle deadly monsters to protect the human race from certain annihilation. A notoriously weak hunter named Sung Jinwoo finds himself in a seemingly endless struggle for survival.",
    #     thumbnail="/en/slider/solo-leveling.jpg",
    #     url="/en/manga/solo-leveling",
    #     language="en"
    # ).save()
    # Manga.objects.all().delete()
    # Chapter.objects.all().delete()
    # for manga in client['en']['manga'].find({}):
    #     manga_obj = Manga(
    #         title=manga['title'],
    #         language="en",
    #         slug=manga['slug'],
    #         description=manga['description'],
    #         thumbnail=manga['thumbnail'],
    #         created_at=make_aware(manga['created_at']),
    #         categories=manga['categories']
    #     )
    #     manga_obj.save()
    #     chapters = [
    #         Chapter(
    #             title=chapter['title'],
    #             slug=chapter['slug'],
    #             created_at=make_aware(manga['created_at']),
    #             pages=chapter['pages']
    #         )
    #         for chapter in manga['chapters']
    #     ]
    #     Chapter.objects.bulk_create(chapters, batch_size=2048)
    #     manga_obj.chapters.add(*chapters)
    #     print(manga['title'], "Success")
