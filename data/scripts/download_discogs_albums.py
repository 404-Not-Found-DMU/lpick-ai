#!/usr/bin/env python3
# data/scripts/download_discogs_albums.py

import os
import argparse
import time
import logging
import csv
import re
from dotenv import load_dotenv
import requests

# 1) .env 로드 (프로젝트 루트의 .env)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '..', '..', '.env')
load_dotenv(ENV_PATH)

# 2) 폴더 구조 설정
RAW_DIR     = os.path.join(BASE_DIR, '..', '..', 'data', 'raw')
DISCOGS_DIR = os.path.join(RAW_DIR, 'discogs')
CSV_DIR     = os.path.join(RAW_DIR, 'csv')
LOG_DIR     = os.path.join(RAW_DIR, 'logs')
for d in (DISCOGS_DIR, CSV_DIR, LOG_DIR):
    os.makedirs(d, exist_ok=True)

# 3) 파일 경로 설정
CSV_PATH = os.path.join(CSV_DIR, 'discogs_albums.csv')
LOG_PATH = os.path.join(LOG_DIR, 'download_discogs_albums.log')

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

# 5) 환경변수 로드
KEY    = os.getenv('DISCOGS_CONSUMER_KEY')
SECRET = os.getenv('DISCOGS_CONSUMER_SECRET')
UA     = 'LpickAI/0.1'

# 6) 검색 대상 목록
ALBUM_QUERIES = [
    {'artist': 'The Beatles', 'album': 'Abbey Road'},
    {'artist': 'Pink Floyd',  'album': 'The Dark Side of the Moon'},
    # … 추가 항목 …
]

# 7) 파일명 안전화 유틸

def sanitize_title(title: str) -> str:
    safe = re.sub(r'[\\/*?:"<>|]', '', title)
    return safe.strip().replace(' ', '_') or 'untitled'

# 8) 이미지 다운로드 함수

def download_image(url: str, dest: str):
    headers = {'User-Agent': UA, 'Referer': 'https://www.discogs.com/'}
    r = requests.get(url, headers=headers, stream=True)
    r.raise_for_status()
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

# 9) REST API 방식 + 페이징 처리 + 전역 카운터 + 이미지 제한

def download_with_rest(query: str, dest_folder: str, csv_writer, csvfile):
    headers = {'User-Agent': UA}
    MAX_IMAGES = 50

    # 첫 요청: 전체 페이지 수 조회
    params = {
        'q':        query,
        'type':     'release',
        'per_page': 100,
        'page':     1,
        'key':      KEY,
        'secret':   SECRET
    }
    r = requests.get('https://api.discogs.com/database/search', params=params, headers=headers)
    r.raise_for_status()
    total_pages = r.json().get('pagination', {}).get('pages', 1)

    seen_urls = set()
    image_counter = 0

    for page in range(1, total_pages + 1):
        logger.info(f"Searching page {page}/{total_pages} for '{query}'")
        params['page'] = page
        resp = requests.get('https://api.discogs.com/database/search', params=params, headers=headers)
        resp.raise_for_status()

        for result in resp.json().get('results', []):
            rid = result.get('id')
            # 상세 조회
            rel_resp = requests.get(f'https://api.discogs.com/releases/{rid}', headers=headers)
            rel_resp.raise_for_status()
            rel = rel_resp.json()

            title    = rel.get('title', '')
            released = rel.get('released', '')
            year     = rel.get('year', '')
            country  = rel.get('country', '')
            genres   = ';'.join(rel.get('genres', []))
            styles   = ';'.join(rel.get('styles', []))
            images   = rel.get('images', [])

            base_name = sanitize_title(title or str(rid))

            for img in images:
                url = img.get('uri')
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                image_counter += 1
                if image_counter > MAX_IMAGES:
                    logger.info(f"Reached {MAX_IMAGES} images for '{query}', moving to next query.")
                    return

                ext = os.path.splitext(url)[1]
                fname = f"{base_name}_{image_counter:04d}{ext}"
                out = os.path.join(dest_folder, fname)

                try:
                    download_image(url, out)
                    logger.info(f"Downloaded image: {fname}")
                except Exception as e:
                    logger.error(f"Error downloading {url}: {e}")
                    continue

                csv_writer.writerow([
                    query.split(' ', 1)[0],
                    query.split(' ', 1)[1] if ' ' in query else '',
                    rid,
                    title,
                    released,
                    year,
                    country,
                    genres,
                    styles,
                    url,
                    fname
                ])
                csvfile.flush()
                time.sleep(1)

        time.sleep(1)

# 10) 메인 실행부

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Discogs 커버 아트 다운로드 (50개 제한)")
    parser.add_argument(
        '--query', help="검색할 앨범 (예: 'Artist Album')"
    )
    parser.add_argument(
        '--dest', default=DISCOGS_DIR,
        help=f"이미지 저장 폴더 (기본: {DISCOGS_DIR})"
    )
    args = parser.parse_args()

    # CSV append 모드 설정
    header_needed = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    mode = 'a' if os.path.exists(CSV_PATH) else 'w'
    with open(CSV_PATH, mode, newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        if header_needed:
            csv_writer.writerow([
                'artist', 'album', 'release_id', 'title', 'released',
                'year', 'country', 'genres', 'styles', 'image_url', 'image_file'
            ])

        tasks = []
        if args.query:
            artist, album = (args.query.split(' ', 1) + [''])[:2]
            tasks.append({'artist': artist, 'album': album})
        else:
            tasks = ALBUM_QUERIES

        for q in tasks:
            query_str = f"{q['artist']} {q['album']}".strip()
            logger.info(f"Processing: {query_str}")
            download_with_rest(query_str, args.dest, csv_writer, csvfile)

    logger.info("모든 작업이 완료되었습니다.")