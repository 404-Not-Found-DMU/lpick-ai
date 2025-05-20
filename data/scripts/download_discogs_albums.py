#!/usr/bin/env python3
# data/scripts/download_discogs_albums.py

import os
import time
import csv
import logging
import re
from dotenv import load_dotenv
import requests

# 1) .env 로드
env_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '.env')
)
load_dotenv(env_path)

# 2) 폴더 구조 설정
RAW_DIR      = os.path.join("data", "raw")
DISCOGS_DIR  = os.path.join(RAW_DIR, "discogs")
CSV_DIR      = os.path.join(RAW_DIR, "csv")
LOG_DIR      = os.path.join(RAW_DIR, "logs")
for d in (DISCOGS_DIR, CSV_DIR, LOG_DIR):
    os.makedirs(d, exist_ok=True)

# 3) 경로 설정
DOWNLOAD_DIR = DISCOGS_DIR
CSV_PATH     = os.path.join(CSV_DIR, "discogs_albums.csv")
LOG_PATH     = os.path.join(LOG_DIR, "download_discogs_albums.log")

# 4) 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Logging to {LOG_PATH} and CSV to {CSV_PATH}")

# 5) Consumer key/secret 로드
CONSUMER_KEY    = os.getenv('DISCOGS_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('DISCOGS_CONSUMER_SECRET')
if not CONSUMER_KEY or not CONSUMER_SECRET:
    logger.error("DISCOGS_CONSUMER_KEY 또는 DISCOGS_CONSUMER_SECRET이 설정되지 않았습니다. .env를 확인하세요.")
    exit(1)

# 6) 검색 대상 목록
ALBUM_QUERIES = [
    {'artist': 'The Beatles', 'album': 'Abbey Road'},
    {'artist': 'Pink Floyd',  'album': 'The Dark Side of the Moon'},
    # … 추가 항목 …
]

# 7) Helper 함수
def sanitize_title(title: str) -> str:
    """앨범 제목을 파일명으로 쓸 수 있도록 안전하게 변환"""
    safe = re.sub(r'[\\/*?:"<>|]', '', title)
    safe = safe.strip().replace(' ', '_')
    return safe or 'untitled'

# 8) Discogs API 호출 함수
def search_album(artist: str, album: str) -> list:
    params = {
        'q':        f"{artist} {album}",
        'type':     'release',
        'per_page': 5,
        'page':     1,
        'key':      CONSUMER_KEY,
        'secret':   CONSUMER_SECRET
    }
    headers = {'User-Agent': 'LpickAI/0.1'}
    resp = requests.get('https://api.discogs.com/database/search', params=params, headers=headers)
    resp.raise_for_status()
    return resp.json().get('results', [])

def fetch_release(release_id: int) -> dict:
    headers = {'User-Agent': 'LpickAI/0.1'}
    resp = requests.get(f'https://api.discogs.com/releases/{release_id}', headers=headers)
    resp.raise_for_status()
    return resp.json()

# 9) 이미지 다운로드 함수
def download_image(url: str, dest: str):
    headers = {
        'User-Agent': 'LpickAI/0.1',
        'Referer': 'https://www.discogs.com/'
    }
    r = requests.get(url, headers=headers, stream=True)
    r.raise_for_status()
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

# 10) 메인 로직

def main():
    # CSV 파일 열기 및 헤더 작성
    logger.info("Opening CSV file for writing...")
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'artist','album','release_id','title','year','genres','styles','image_url','image_file'
        ])

        for q in ALBUM_QUERIES:
            artist, album = q['artist'], q['album']
            logger.info(f"Searching Discogs: {artist} – {album}")
            try:
                results = search_album(artist, album)
            except Exception as e:
                logger.error(f"Search failed for {artist} – {album}: {e}")
                continue

            for res in results:
                rid     = res['id']
                release = fetch_release(rid)

                title  = release.get('title', '')
                year   = release.get('year', '')
                genres = ';'.join(release.get('genres', []))
                styles = ';'.join(release.get('styles', []))
                images = release.get('images', [])

                # 제목 안전화
                base_name = sanitize_title(title or str(rid))

                # 이미지별 저장 및 CSV 기록
                for img in images:
                    url = img.get('uri')
                    ext = os.path.splitext(url)[1]

                    # prefix에 숫자 suffix 붙이기
                    existing = [f for f in os.listdir(DOWNLOAD_DIR)
                                if f.startswith(base_name + '_') and f.endswith(ext)]
                    count = len(existing) + 1
                    fname = f"{base_name}_{count:02d}{ext}"
                    out = os.path.join(DOWNLOAD_DIR, fname)

                    try:
                        download_image(url, out)
                        logger.info(f"Downloaded image: {fname}")
                    except Exception as e:
                        logger.error(f"Error downloading {url}: {e}")
                        continue

                    # CSV 기록
                    writer.writerow([artist, album, rid, title, year, genres, styles, url, fname])
                    csvfile.flush()

                    time.sleep(1)

            time.sleep(1)

if __name__ == '__main__':
    main()
