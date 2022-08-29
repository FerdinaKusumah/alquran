from typing import List

import requests
import strawberry
from cachetools import cached, LRUCache
from pydantic import parse_obj_as

from models import (
    SurahModel,
    AyahModel,
)

session = requests.session()
BASE_URL = "https://quran.kemenag.go.id"


@cached(cache=LRUCache(maxsize=1024))
def fetch_data_surah():
    resp = session.get("{base_url}/api/v1/surah".format(base_url=BASE_URL)).json()
    return resp["data"]


@cached(cache=LRUCache(maxsize=1024))
def fetch_data_ayah(surah_id: int):
    all_ayah = fetch_data_surah()
    ayah = list(filter(lambda x: x["id"] == surah_id, all_ayah))
    if len(ayah) == 0:
        return []

    resp = session.get(
        "{base_url}/api/v1/ayatweb/{surah_id}/0/0/{count_ayah}".format(
            base_url=BASE_URL, surah_id=surah_id, count_ayah=ayah[0]["count_ayat"]
        )
    ).json()
    return resp["data"]


@cached(cache=LRUCache(maxsize=1024))
def fetch_ayah_sound(surah_id: int, ayah_id: int) -> str:
    resp = session.get(
        "{base_url}/cmsq/source/s01/{surah_id}{ayah_id}.mp3".format(
            base_url=BASE_URL,
            surah_id=str(surah_id).zfill(3),
            ayah_id=str(ayah_id).zfill(3),
        ),
        stream=True,
    ).text
    return resp


def all_surah() -> List["SurahSchema"]:
    resp = fetch_data_surah()
    obj = parse_obj_as(List[SurahModel], resp)
    return [SurahSchema.from_pydantic(doc) for doc in obj]


def surah(surah_id: int) -> List["SurahSchema"]:
    resp = list(filter(lambda x: x["id"] == surah_id, fetch_data_surah()))
    obj = parse_obj_as(List[SurahModel], resp)
    return [SurahSchema.from_pydantic(doc) for doc in obj]


def ayah(surah_id: int) -> List["AyahSchema"]:
    resp = fetch_data_ayah(surah_id)
    obj = parse_obj_as(List[AyahModel], resp)
    return [AyahSchema.from_pydantic(doc) for doc in obj]


@strawberry.experimental.pydantic.type(model=SurahModel)
class SurahSchema:
    id: strawberry.auto
    surah_name: strawberry.auto
    surah_text: strawberry.auto
    surah_translate: strawberry.auto
    surah_type: strawberry.auto
    count_ayah: strawberry.auto


@strawberry.experimental.pydantic.type(model=AyahModel)
class AyahSchema:
    id: strawberry.auto
    surah_number: strawberry.auto
    ayah_number: strawberry.auto
    ayah_text: strawberry.auto
    ayah_theme: strawberry.auto
    ayah_translate: strawberry.auto
    no_fn: strawberry.auto
    teks_fn: strawberry.auto


@strawberry.type
class Query:
    all_surah: List[SurahSchema] = strawberry.field(resolver=all_surah)

    @strawberry.field
    def surah(self, surah_id: int) -> List[SurahSchema]:
        return surah(surah_id)

    @strawberry.field
    def sound(self, surah_id: int, ayah_id: int) -> str:
        return fetch_ayah_sound(surah_id, ayah_id)

    @strawberry.field
    def ayah(self, surah_id: int) -> List[AyahSchema]:
        return ayah(surah_id)
