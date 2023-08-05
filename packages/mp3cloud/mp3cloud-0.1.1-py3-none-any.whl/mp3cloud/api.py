"""API utils"""

from typing import List

# import requests
from bs4 import BeautifulSoup
from .objects import Song
from .utils import shell_call


home_url = "https://freemp3cloud.com/"


cookies = {
    "__ddg2_": "OoNQEIynYTMJoVwU",
    "__ddg1_": "9NZlynXQBBht02meCgQe",
    "_ym_uid": "1669227862874709378",
    ".AspNetCore.Antiforgery.2kyQ2nmXF04": "CfDJ8JKPcoD1_8lEtTdrfYWqW-lcrqTxTPlY2MpWV3ii0eqR_t8QkYs-NGxFjaBu16S4r6GlnTRPRyqmtlOBwFy9kkdg7bPp5rF_J-a8zJwrwySY6lYjG2VlWnQGK6G9C5NU6cpWrIltLwN9IjQuOq_mSmk",
    "_ym_isad": "1",
}

home_headers = {
    "authority": "wwv.freemp3cloud.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}


search_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "__ddgid_=1oM5Id8xmdtHEaYE; __ddg2_=f6iCngi4ZDzNjOC8; __ddg1_=rxcm6FzD6RuNipsDKO9D; .AspNetCore.Antiforgery.2kyQ2nmXF04=CfDJ8NzsyqJ783FKu4o7QZmkp9gQzwa-ZnkL0uMvoFmjo8Mphvmwo7_2fRf1pQeTrTlQb3uSb1vuGX_KjBV90sJVQn2HCWI8wdKlNqLmnUHT7STwrYCbvuSZ_tFvO0lOx3LiPJOPuBGMdcwcbFbLeqZWNKk",
    "Referer": "https://vww.freemp3cloud.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}


# session = requests.Session()


# def get_soup(url: str, headers: dict = None):
#     r = session.get(url, headers=headers, cookies=cookies)
#     r.raise_for_status()
#     return BeautifulSoup(r.text, "html.parser")


def get_token() -> str:
    # soup = get_soup(home_url, home_headers)
    text = shell_call("token.sh")
    soup = BeautifulSoup(text, "html.parser")
    token = soup.find("input", {"name": "__RequestVerificationToken"}).get("value")
    return token


def get_search_soup(q: str):
    q = q.replace(" ", "+")
    # data = {"searchSong": q, "__RequestVerificationToken": get_token()}
    # r = session.post(home_url, data, headers=search_headers)
    # r.raise_for_status()
    text = shell_call(f"search.sh {q}")
    soup = BeautifulSoup(text, "html.parser")
    return soup


def search(q: str, limit: int = None) -> List[Song]:
    """Searches and returns a list of `fcloud.objects.Song`s for the given query if available on the site."""
    soup = get_search_soup(q)
    tags = soup.find_all("div", {"class": "play-item"}, limit=limit)
    songs = []
    for tag in tags:
        name = tag.find("div", {"class": "s-title"}).get_text()
        artist = tag.find("div", {"class": "s-artist"}).get_text()
        url = tag.find("div", {"class": "downl"}).find("a")["href"]
        duration = tag.find("div", {"class": "s-time"}).get_text()
        is_high_quality = tag.find("div", {"class": "s-hq"}) is not None
        song = Song(
            name=name,
            artist=artist,
            url=url,
            duration=duration,
            is_high_quality=is_high_quality,
        )
        songs.append(song)
    return songs
