# AI_LP_Search_Project

## 프로젝트 개요

AI_LP_Search_Project는 **LP 이미지 기반 검색 시스템**입니다. 사용자가 업로드한 LP 앨범 이미지와 관련 정보를 비교하여, **이미지 유사도 기반 검색** 및 **OCR(이미지 내 텍스트 추출)** 기반 검색/추천 기능을 제공하는 AI 시스템입니다.

---

## 🛠️ 사용 기술 스택

- **Python**: 개발 언어
- **Torch, torchvision**: 딥러닝 모델 구축
- **OpenCV**: 이미지 전처리
- **FAISS**: 임베딩 기반 검색
- **Flask** → **FastAPI**: API 서버 프레임워크
- **Jupyter Notebook**: 데이터 탐색 및 실험
- **Pandas, Numpy**: 데이터 처리
- **Matplotlib**: 시각화 도구

---

## 📁 폴더 구조 및 역할

```plaintext
📦lpick-ai
 ┣ 📂.git
 ┃ ┣ 📂hooks
 ┃ ┃ ┣ 📜applypatch-msg.sample
 ┃ ┃ ┣ 📜commit-msg.sample
 ┃ ┃ ┣ 📜fsmonitor-watchman.sample
 ┃ ┃ ┣ 📜post-update.sample
 ┃ ┃ ┣ 📜pre-applypatch.sample
 ┃ ┃ ┣ 📜pre-commit.sample
 ┃ ┃ ┣ 📜pre-merge-commit.sample
 ┃ ┃ ┣ 📜pre-push.sample
 ┃ ┃ ┣ 📜pre-rebase.sample
 ┃ ┃ ┣ 📜pre-receive.sample
 ┃ ┃ ┣ 📜prepare-commit-msg.sample
 ┃ ┃ ┣ 📜push-to-checkout.sample
 ┃ ┃ ┗ 📜update.sample
 ┃ ┣ 📂info
 ┃ ┃ ┗ 📜exclude
 ┃ ┣ 📂logs
 ┃ ┃ ┣ 📂refs
 ┃ ┃ ┃ ┣ 📂heads
 ┃ ┃ ┃ ┃ ┗ 📜main
 ┃ ┃ ┃ ┗ 📂remotes
 ┃ ┃ ┃ ┃ ┗ 📂origin
 ┃ ┃ ┃ ┃ ┃ ┗ 📜HEAD
 ┃ ┃ ┗ 📜HEAD
 ┃ ┣ 📂objects
 ┃ ┃ ┣ 📂info
 ┃ ┃ ┗ 📂pack
 ┃ ┃ ┃ ┣ 📜pack-f0fee847fa7494eef58b64457320538f47d1c888.idx
 ┃ ┃ ┃ ┗ 📜pack-f0fee847fa7494eef58b64457320538f47d1c888.pack
 ┃ ┣ 📂refs
 ┃ ┃ ┣ 📂heads
 ┃ ┃ ┃ ┗ 📜main
 ┃ ┃ ┣ 📂remotes
 ┃ ┃ ┃ ┗ 📂origin
 ┃ ┃ ┃ ┃ ┗ 📜HEAD
 ┃ ┃ ┗ 📂tags
 ┃ ┣ 📜FETCH_HEAD
 ┃ ┣ 📜HEAD
 ┃ ┣ 📜config
 ┃ ┣ 📜description
 ┃ ┣ 📜index
 ┃ ┗ 📜packed-refs
 ┣ 📂config
 ┃ ┣ 📜config.yaml
 ┃ ┗ 📜logging.yaml
 ┣ 📂data
 ┃ ┣ 📂external
 ┃ ┣ 📂processed
 ┃ ┣ 📂raw
 ┃ ┗ 📂scripts
 ┃ ┃ ┗ 📜preprocess_data.py
 ┣ 📂logs
 ┃ ┗ 📜training.log
 ┣ 📂models
 ┃ ┣ 📂checkpoints
 ┃ ┣ 📂model_architectures
 ┃ ┃ ┣ 📜clip_model.py
 ┃ ┃ ┗ 📜resnet_model.py
 ┃ ┣ 📂saved_models
 ┃ ┣ 📂scripts
 ┃ ┃ ┣ 📜evaluate_model.py
 ┃ ┃ ┗ 📜train_model.py
 ┃ ┗ 📂utils
 ┃ ┃ ┗ 📜image_utils.py
 ┣ 📂notebooks
 ┃ ┣ 📜EDA.ipynb
 ┃ ┗ 📜model_training.ipynb
 ┣ 📂src
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📜inference.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┗ 📜search.py
 ┃ ┣ 📂data_loader
 ┃ ┃ ┣ 📜image_loader.py
 ┃ ┃ ┗ 📜text_loader.py
 ┃ ┣ 📂features
 ┃ ┃ ┗ 📜feature_extraction.py
 ┃ ┣ 📂models
 ┃ ┃ ┣ 📜clip_model.py
 ┃ ┃ ┣ 📜ocr_model.py
 ┃ ┃ ┗ 📜resnet_model.py
 ┃ ┣ 📂utils
 ┃ ┃ ┣ 📜cosine_similarity.py
 ┃ ┃ ┗ 📜ocr_utils.py
 ┃ ┗ 📂visualization
 ┃ ┃ ┗ 📜plot_results.py
 ┣ 📂tests
 ┃ ┣ 📂test_api
 ┃ ┃ ┗ 📜test_inference.py
 ┃ ┣ 📂test_data
 ┃ ┃ ┗ 📜test_preprocess_data.py
 ┃ ┗ 📂test_models
 ┃ ┃ ┗ 📜test_clip_model.py
 ┣ 📜.gitignore
 ┣ 🐳Dockerfile
 ┣ 📜README.md
 ┣ 📜environment.yml
 ┗ 📜requirements.txt
```

### 1. `data/` - 데이터 관리

- `raw/`: 원본 이미지 및 텍스트
- `processed/`: 전처리된 데이터 (크기 조정, 정제 등)
- `external/`: 외부 LP 공개 데이터셋
- `scripts/`: 전처리 스크립트 (`preprocess_data.py`)

### 2. `notebooks/` - 분석 및 실험

- `EDA.ipynb`: 탐색적 데이터 분석
- `model_training.ipynb`: 모델 학습/실험 (CLIP, ResNet, DINOv2)

### 3. `models/` - 모델 정의 및 저장

- `checkpoints/`: 훈련 중간 저장 모델
- `saved_models/`: 최종 학습 모델
- `model_architectures/`: 모델 아키텍처 정의 (`clip_model.py`, `resnet_model.py`)
- `scripts/`: 학습/평가 스크립트 (`train_model.py`, `evaluate_model.py`)
- `utils/`: 이미지 처리 유틸 (`image_utils.py`)

### 4. `src/` - 핵심 로직 구현

- `api/`: API 서버 (`main.py`, `inference.py`, `search.py`)
- `data_loader/`: 데이터 로딩 (`image_loader.py`, `text_loader.py`)
- `features/`: 특징 추출 (`feature_extraction.py`)
- `models/`: CLIP, ResNet, OCR 모델 정의
- `utils/`: 공통 유틸 (`cosine_similarity.py`, `ocr_utils.py`)
- `visualization/`: 결과 시각화 (`plot_results.py`)

### 5. `tests/` - 테스트 코드

- 모델 테스트: `test_models/`
- 데이터 테스트: `test_data/`
- API 테스트: `test_api/`

### 6. 기타 주요 파일

- `Dockerfile`: Docker 설정
- `requirements.txt`: 패키지 목록
- `environment.yml`: Conda 환경 설정
- `config.yaml`, `logging.yaml`: 프로젝트 설정 및 로깅
- `training.log`: 학습 로그
- `README.md`: 프로젝트 설명 문서

---

## 💻 설치 및 실행 방법

### 1. 가상환경 및 패키지 설치

```bash
# pip 사용 시
pip install -r requirements.txt

# Conda 사용 시
conda env create -f environment.yml
```

### 2. 모델 훈련

- `notebooks/model_training.ipynb` 열고 학습 실행

### 3. 데이터 전처리

```bash
python data/scripts/preprocess_data.py
```

### 4. API 서버 실행

```bash
uvicorn src.api.main:app --reload
```
