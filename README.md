# lpick-ai

🎵 LPick AI 코드 저장소입니다.

---

## 📌 프로젝트 개요

LP 음반(레코드판) 이미지를 검색하고, 텍스트를 기반으로 검색할 수 있는 AI 기반 검색 시스템을 구축합니다.  
향후 학습된 모델을 FastAPI 서버에 연결하여 사용자 요청에 대해 실시간 검색 결과를 제공할 예정입니다.

---

## 🛠️ 사용 기술 스택

- **Python** : 개발 언어
- **Torch, torchvision** : 딥러닝 모델 구축
- **OpenCV** : 이미지 전처리
- **FAISS** : 임베딩 기반 검색
- **Flask (초기 테스트)** → **FastAPI (최종 서버화)**
- **Jupyter Notebook** : 데이터 탐색 및 모델 개발
- **Pandas, Numpy** : 데이터 처리
- **Matplotlib** : 시각화 도구

---

## 📁 프로젝트 폴더 구조

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

---

## ✅ 지금까지 진행한 사항

## 🚀 전체 진행 체크리스트

- [x] **1단계: 가상환경(venv) 생성 및 세팅**
  - `python -m venv venv`로 프로젝트 가상환경 생성
- [x] **2단계: 가상환경 활성화 및 pip 업그레이드**
  - `source venv/bin/activate` 및 `pip install --upgrade pip`
- [x] **3단계: 필수 패키지 설치**
  - torch, torchvision, opencv-python, faiss-cpu 등 설치
- [x] **4단계: requirements.txt 생성**
  - `pip freeze > requirements.txt`로 패키지 목록 저장
- [x] **5단계: .gitignore 파일 작성 및 최적화**
  - venv, 로그파일, 모델결과물, 개인설정 등 제외 처리
- [x] **6단계: develop 브랜치 생성 및 Git 세팅**
  - main → develop 분기, 작업 브랜치 전략 설정
- [x] **7단계: config.yaml 파일 작성**
  - 데이터 경로, 모델 경로 등 설정 파일 구성
- [x] **8단계: EDA.ipynb 작성 및 탐색적 데이터 분석**
  - 이미지/텍스트 수 확인, 샘플 시각화, 깨진 파일 검출
- [ ] **9단계: 데이터 전처리 (Preprocessing)**
  - 이미지 리사이징, 정규화, 텍스트 정제 등
- [ ] **10단계: 특징 추출 (Feature Extraction)**
  - CLIP, ResNet, DINOv2 등을 활용한 임베딩 벡터 추출
- [ ] **11단계: 모델 학습 (Training)**
  - 학습 및 필요시 파인튜닝 진행
- [ ] **12단계: 모델 저장 및 추론(Inference) 코드 작성**
  - 학습된 모델을 저장하고 Inference API 준비
- [ ] **13단계: FastAPI 서버 구축**
  - 사용자 요청을 처리할 API 서버 구축
- [ ] **14단계: 전체 통합 테스트**
  - 데이터 → 모델 → 서버 → 결과까지 전체 연동 점검

---

## 🧠 전체 개발 흐름 요약

---

## ✨ 기타 주의사항

- 모든 개발은 `venv` 가상환경 하에서 진행합니다.
- 설치 패키지는 `requirements.txt`로 관리합니다.
- 각 작업 단계별로 Git 브랜치를 생성하여 독립적으로 개발합니다.
- PR 작성 시 명확한 제목과 작업 요약을 작성합니다.
- FastAPI 서버는 추후 `src/api/` 경로에 구축될 예정입니다.

---

# 🏁 최종 목표

**LP 음반 검색 AI 시스템 구축**

- **FastAPI 서버를 통해 사용자 요청에 대해 빠르게 검색 결과를 반환하는 서비스 제공**
```
