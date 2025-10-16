# 📌 이슈: LP 앨범 이미지 검색 시스템 구축

## ✨ 기능 설명

크롤링한 약 80,000개의 LP 앨범 이미지를 기반으로 **이미지 유사도 검색 시스템**을 구축합니다. 사용자가 LP 앨범 이미지를 업로드하면, 데이터베이스에서 가장 유사한 이미지들을 찾아 메타데이터(앨범명, 아티스트, 장르 등)와 함께 반환하는 시스템입니다.

**핵심 기능:**

- 이미지 기반 유사 이미지 검색
- 텍스트 기반 이미지 검색 (CLIP 사용 시)
- 장르, 년도 등 필터링 기능
- 웹 UI를 통한 직관적인 검색 인터페이스

## ✅ 세부 작업 항목

### 1단계: 데이터 전처리 및 분석 📊

- [ ] 크롤링된 이미지 데이터 현황 분석 스크립트 작성
  - 장르별 이미지 개수 통계
  - 이미지 크기/해상도 분포 분석
  - 손상된 이미지 감지 및 제거
- [ ] CSV 메타데이터 통합 및 정리
  - 14개 장르별 CSV 파일 병합
  - 데이터 클렌징 (중복 제거, 결측치 처리)
  - 통합 메타데이터 JSON/CSV 생성
- [ ] EDA (탐색적 데이터 분석) 노트북 작성
  - 샘플 이미지 시각화
  - 장르별 분포 차트
  - 데이터 품질 리포트

**예상 시간:** 1-2시간  
**담당 파일:** `tools/analysis/analyze_crawled_data.py`, `notebooks/image_search_eda.ipynb`

---

### 2단계: 이미지 임베딩 모델 선택 및 테스트 🤖

- [ ] 이미지 임베딩 모델 비교 분석
  - CLIP (OpenAI) - 멀티모달 ⭐ 추천
  - ResNet50 (ImageNet pretrained)
  - DINOv2 (Meta)
- [ ] 선택한 모델 다운로드 및 환경 설정
- [ ] 샘플 이미지로 임베딩 생성 테스트
  - 임베딩 차원 확인
  - 처리 속도 측정
  - 메모리 사용량 체크
- [ ] 모델 래퍼 클래스 작성 (`models/model_architectures/embedding_model.py`)

**예상 시간:** 1-2시간  
**담당 파일:** `models/model_architectures/embedding_model.py`, `notebooks/model_selection.ipynb`

---

### 3단계: 전체 이미지 임베딩 생성 💾

- [ ] 배치 임베딩 생성 스크립트 작성
  - GPU 활용 최적화
  - 배치 처리 (batch_size 조절)
  - 진행상황 로깅 (tqdm 사용)
- [ ] 재시작 가능한 체크포인트 시스템 구현
  - 이미 처리된 이미지 스킵
  - 중간 저장 기능
- [ ] 전체 80,000개 이미지 임베딩 생성 실행
- [ ] 임베딩 벡터 저장
  - numpy 배열로 저장 (`.npy`)
  - 메타데이터 매핑 파일 생성 (`image_id -> metadata`)

**예상 시간:** 2-4시간 (GPU 사용 시)  
**담당 파일:** `scripts/generate_embeddings.py`  
**출력 위치:** `data/processed/embeddings/`

---

### 4단계: FAISS 벡터 검색 인덱스 구축 🔍

- [ ] FAISS 라이브러리 설치 및 설정
  - `pip install faiss-cpu` or `faiss-gpu`
- [ ] FAISS 인덱스 생성 스크립트 작성
  - IndexFlatL2 (정확도 우선)
  - IndexIVFFlat (속도 우선)
  - 인덱스 타입 비교 실험
- [ ] 임베딩 벡터를 FAISS 인덱스로 변환
- [ ] 인덱스 저장 및 로드 기능 구현
- [ ] 검색 성능 벤치마크
  - Top-K 검색 속도 측정 (K=5, 10, 20)
  - 검색 정확도 평가

**예상 시간:** 1-2시간  
**담당 파일:** `src/features/faiss_indexer.py`  
**출력 위치:** `data/processed/faiss_index/`

---

### 5단계: 검색 API 개발 🌐

- [ ] FastAPI 서버 구조 설계
- [ ] API 엔드포인트 구현
  - `POST /search/image` - 이미지 업로드 검색
  - `POST /search/text` - 텍스트 기반 검색 (CLIP)
  - `GET /image/{image_id}` - 이미지 메타데이터 조회
  - `GET /stats` - 데이터베이스 통계
- [ ] 이미지 전처리 파이프라인
  - 이미지 리사이징
  - 정규화 (normalization)
- [ ] 검색 결과 포맷팅
  - 유사도 점수 포함
  - 메타데이터 (앨범명, 아티스트, 장르 등)
  - 이미지 URL/경로
- [ ] 에러 핸들링 및 로깅
- [ ] API 문서 자동 생성 (Swagger/OpenAPI)

**예상 시간:** 2-3시간  
**담당 파일:** `src/api/search_api.py`, `src/api/main.py`

**API 스펙 예시:**

```json
POST /search/image
Request: multipart/form-data (image file)
Response: {
  "results": [
    {
      "image_id": "Blues_000123",
      "similarity": 0.95,
      "metadata": {
        "title": "Blues Brothers",
        "artist": "Various",
        "genre": "Blues",
        "year": 1980
      },
      "image_url": "/images/Blues/..."
    }
  ],
  "query_time_ms": 45
}
```

---

### 6단계: 웹 UI 개발 🎨

- [ ] HTML/CSS/JavaScript 프론트엔드 구조 설계
- [ ] 이미지 업로드 페이지 구현
  - 드래그 앤 드롭 지원
  - 이미지 미리보기
  - 파일 크기/형식 검증
- [ ] 검색 결과 표시 페이지
  - 그리드 레이아웃 (responsive)
  - 유사도 점수 표시
  - 메타데이터 팝업/모달
- [ ] 필터링 기능
  - 장르 선택
  - 년도 범위
  - 유사도 임계값
- [ ] 텍스트 검색 인터페이스 (CLIP 사용 시)
- [ ] 로딩 상태 및 에러 메시지 UI
- [ ] 반응형 디자인 (모바일/태블릿 지원)

**예상 시간:** 3-4시간  
**담당 파일:** `templates/image_search.html`, `static/css/search.css`, `static/js/search.js`

---

### 7단계: 테스트 및 최적화 ⚡

- [ ] 유닛 테스트 작성
  - 임베딩 생성 테스트
  - FAISS 인덱스 테스트
  - API 엔드포인트 테스트
- [ ] 통합 테스트
  - End-to-End 검색 플로우 테스트
- [ ] 성능 테스트
  - 검색 속도 벤치마크
  - 동시 요청 처리 테스트
  - 메모리 프로파일링
- [ ] 최적화
  - 임베딩 캐싱 전략
  - API 응답 캐싱 (Redis)
  - 이미지 로딩 최적화 (lazy loading)
- [ ] 검색 품질 평가
  - 수동 평가 (샘플 이미지로 테스트)
  - 유사도 임계값 조정

**예상 시간:** 2-3시간  
**담당 파일:** `tests/test_image_search/`

---

### 8단계: 배포 및 문서화 📚

- [ ] Docker 컨테이너화
  - Dockerfile 작성
  - docker-compose.yml 구성
- [ ] 배포 가이드 작성
  - 환경 설정
  - 실행 방법
  - API 사용 예시
- [ ] 사용자 문서 작성
  - README 업데이트
  - API 문서
  - 트러블슈팅 가이드
- [ ] 데모 영상/스크린샷 준비

**예상 시간:** 2-3시간  
**담당 파일:** `README.md`, `docs/IMAGE_SEARCH.md`

---

## 📊 전체 일정 및 우선순위

| 단계 | 작업                  | 우선순위 | 예상 시간 | 상태      |
| ---- | --------------------- | -------- | --------- | --------- |
| 1    | 데이터 전처리 및 분석 | 🔴 높음  | 1-2h      | ✅ 완료   |
| 2    | 모델 선택 및 테스트   | 🔴 높음  | 1-2h      | ✅ 완료   |
| 3    | 임베딩 생성           | 🔴 높음  | 2-4h      | ✅ 완료   |
| 4    | FAISS 인덱스 구축     | 🟡 중간  | 1-2h      | 🔄 진행중 |
| 5    | 검색 API 개발         | 🟡 중간  | 2-3h      | ⏳ 대기   |
| 6    | 웹 UI 개발            | 🟢 낮음  | 3-4h      | ⏳ 대기   |
| 7    | 테스트 및 최적화      | 🟡 중간  | 2-3h      | ⏳ 대기   |
| 8    | 배포 및 문서화        | 🟢 낮음  | 2-3h      | ⏳ 대기   |

**총 예상 시간:** 14-23시간

---

## 🧩 참고 자료

### 기술 문서

- [CLIP (OpenAI)](https://github.com/openai/CLIP) - 멀티모달 이미지-텍스트 모델
- [FAISS (Facebook AI)](https://github.com/facebookresearch/faiss) - 고속 유사도 검색 라이브러리
- [FastAPI 문서](https://fastapi.tiangolo.com/) - 최신 Python 웹 프레임워크
- [ResNet 논문](https://arxiv.org/abs/1512.03385) - 이미지 분류 모델
- [DINOv2 (Meta)](https://github.com/facebookresearch/dinov2) - Self-supervised 비전 모델

### 유사 프로젝트

- [Reverse Image Search with CLIP](https://github.com/haltakov/natural-language-image-search)
- [Image Search Engine using FAISS](https://github.com/matsui528/sis)

### 내부 문서

- `FOLDER_STRUCTURE.md` - 프로젝트 구조 설명
- `REORGANIZATION.md` - 최근 폴더 정리 내역
- `data/raw/csv/*.csv` - 크롤링 메타데이터
- `notebooks/EDA.ipynb` - 초기 데이터 분석

---

## 🚀 시작하기

### 즉시 시작 가능한 작업

1. **데이터 현황 분석 스크립트 실행**

   ```bash
   python tools/analysis/analyze_crawled_data.py
   ```

2. **모델 선택을 위한 실험**

   ```bash
   jupyter notebook notebooks/model_selection.ipynb
   ```

3. **환경 설정**
   ```bash
   pip install torch torchvision transformers faiss-cpu pillow
   ```

---

## 📝 진행 상황 업데이트

- **2024-10-16 09:00**: 이슈 생성, 프로젝트 구조 정리 완료
- **2024-10-16 09:30**: ✅ 1단계 완료 - 데이터 분석 (86,171개 이미지 확인)
- **2024-10-16 10:00**: ✅ 2단계 완료 - 모델 선택 (CLIP 선택 결정)
- **2024-10-16 10:39**: ✅ 3단계 완료 - 임베딩 생성 (86,171개, 168MB, 36.2분 소요)
- **2024-10-16 10:40**: 🔄 4단계 시작 예정 - FAISS 인덱스 구축

---

## 💬 논의 사항

- [ ] 임베딩 모델 최종 선택: CLIP vs ResNet50 vs DINOv2
- [ ] FAISS 인덱스 타입: 정확도 vs 속도 trade-off
- [ ] API 응답 시간 목표: 100ms? 500ms? 1s?
- [ ] 웹 UI 프레임워크: Vanilla JS vs React vs Vue
- [ ] 배포 환경: 로컬 서버 vs 클라우드 (AWS/GCP)

---

## 🎯 성공 기준

- [ ] 80,000개 이미지 임베딩 생성 완료
- [ ] 검색 API 응답 시간 < 500ms
- [ ] 검색 정확도 주관 평가 > 80% 만족도
- [ ] 웹 UI에서 이미지 업로드 및 검색 가능
- [ ] 문서화 완료 (README, API docs)
- [ ] Docker로 배포 가능

---

## 👥 담당자

- **개발:** @kogun
- **리뷰:** TBD
- **테스트:** TBD
