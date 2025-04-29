# AI_LP_Search_Project

## 프로젝트 개요

AI_LP_Search_Project는 **LP 이미지 기반 검색 시스템**입니다. 이 프로젝트는 사용자가 업로드한 이미지와 LP 앨범 관련 정보를 비교하여, 이미지 유사도 기반으로 관련 LP 정보를 검색하는 시스템을 구축합니다. 또한 **OCR**(이미지 내 텍스트 추출) 기술을 활용하여 LP 이미지에서 텍스트를 추출하고 이를 기반으로 검색 및 추천 시스템을 구현합니다.

## 폴더 구조

### 1. **data/** - 데이터 관련 폴더

이 폴더는 프로젝트에서 사용하는 모든 데이터와 데이터 전처리 스크립트가 포함됩니다.

- **raw/**: 원시 데이터 (이미지 및 텍스트 데이터)
  - 프로젝트에서 사용되는 원본 이미지를 이 폴더에 저장합니다.
- **processed/**: 전처리된 데이터 (이미지 전처리, 텍스트 정제 등)
  - 전처리된 데이터는 모델 훈련에 사용됩니다. 이미지 크기 조정, OCR 텍스트 정제 등의 작업을 거친 데이터를 저장합니다.
- **external/**: 외부 데이터셋 (공개 LP 데이터셋)
  - 외부에서 다운로드한 공개 LP 데이터셋이 저장됩니다.
- **scripts/**: 데이터 전처리 관련 스크립트
  - `preprocess_data.py`: 데이터 전처리 스크립트로, 이미지 크기 조정, OCR 텍스트 정제, 데이터 정리 등을 수행합니다.

### 2. **notebooks/** - Jupyter notebooks 폴더

프로젝트의 데이터 분석, 모델 훈련 및 실험을 위한 Jupyter Notebook 파일들이 포함됩니다.

- **EDA.ipynb**: 탐색적 데이터 분석 (EDA) 노트북. 데이터를 분석하고, 특성에 대한 이해를 돕는 코드와 시각화가 포함됩니다.
- **model_training.ipynb**: 모델 훈련 및 실험을 위한 노트북. **CLIP**, **ResNet**, **DINOv2** 모델을 훈련시키고 평가하는 코드가 포함됩니다.

### 3. **models/** - 모델 관련 폴더

모델 정의 및 훈련, 평가와 관련된 파일들이 포함됩니다.

- **checkpoints/**: 모델 훈련 중 저장된 체크포인트
  - 훈련 중간에 저장되는 모델의 상태가 저장됩니다. 훈련이 중단되면, 이 체크포인트에서 다시 시작할 수 있습니다.
- **saved_models/**: 훈련 완료 모델
  - 최종 훈련된 모델이 저장되는 폴더입니다.
- **model_architectures/**: 모델 아키텍처 정의
  - 모델을 정의한 코드 파일들 (예: CLIP, ResNet 모델 등).
  - `clip_model.py`: **CLIP** 모델 아키텍처를 정의한 파일입니다.
  - `resnet_model.py`: **ResNet** 모델 아키텍처를 정의한 파일입니다.
- **scripts/**: 모델 훈련 및 평가 스크립트
  - `train_model.py`: 모델 훈련 스크립트로, 데이터셋을 불러와서 모델을 훈련시킵니다.
  - `evaluate_model.py`: 훈련된 모델을 평가하는 스크립트입니다.
- **utils/**: 모델 관련 유틸리티 함수
  - `image_utils.py`: 이미지 전처리 및 특징 추출을 위한 유틸리티 함수들이 포함됩니다.

### 4. **src/** - 실제 코드 및 로직 폴더

애플리케이션의 핵심 코드와 관련된 파일들이 포함됩니다.

- **api/**: FastAPI/Flask API 서버 관련 코드
  - `main.py`: FastAPI 또는 Flask 앱 초기화 코드입니다.
  - `inference.py`: 모델 예측을 처리하는 엔드포인트를 구현한 파일입니다.
  - `search.py`: 이미지 유사도 검색 엔드포인트를 구현한 파일입니다.
- **data_loader/**: 데이터 로딩 및 전처리 관련 코드
  - `image_loader.py`: 이미지 로딩 및 전처리 코드입니다.
  - `text_loader.py`: OCR 결과로 추출된 텍스트 데이터를 로딩하는 코드입니다.
- **features/**: 이미지 및 텍스트 특징 추출
  - `feature_extraction.py`: 이미지 및 텍스트의 특징을 추출하는 함수가 포함됩니다.
- **models/**: 모델 정의 및 로직
  - `clip_model.py`: CLIP 모델을 정의한 코드입니다.
  - `resnet_model.py`: ResNet 모델을 정의한 코드입니다.
  - `ocr_model.py`: OCR 모델을 정의한 코드입니다.
- **utils/**: 공통 유틸리티 함수들
  - `cosine_similarity.py`: **Cosine Similarity**를 사용한 유사도 계산 함수입니다.
  - `ocr_utils.py`: OCR 후처리 및 텍스트 정제 함수들이 포함됩니다.
- **visualization/**: 결과 시각화 관련 코드
  - `plot_results.py`: 모델 평가 결과를 시각화하는 코드입니다.

### 5. **tests/** - 테스트 관련 폴더

프로젝트의 각 기능에 대한 **단위 테스트** 및 **통합 테스트**가 포함됩니다.

- **test_models/**: 모델 테스트
  - `test_clip_model.py`: **CLIP** 모델에 대한 단위 테스트 코드입니다.
- **test_data/**: 데이터 전처리 테스트
  - `test_preprocess_data.py`: 데이터 전처리 기능에 대한 단위 테스트 코드입니다.
- **test_api/**: API 테스트
  - `test_inference.py`: API 예측 엔드포인트에 대한 테스트 코드입니다.

### 6. **기타 주요 파일**

- **Dockerfile**: 프로젝트를 **Docker 컨테이너화**하여 배포할 수 있도록 설정하는 파일입니다.
- **requirements.txt**: 프로젝트에서 필요한 **Python 패키지 목록**을 기록한 파일입니다.
- **environment.yml**: Conda 환경 설정 파일입니다. Conda 환경을 설정할 때 사용됩니다.
- **config/**: 설정 파일 폴더
  - `config.yaml`: 프로젝트 설정(하이퍼파라미터, 데이터 경로 등) 및 환경 설정이 포함된 YAML 파일입니다.
  - `logging.yaml`: 로깅 설정 파일로, 로그의 수준 및 저장 위치를 정의합니다.
- **logs/**: 훈련 로그 및 기타 중요 로그를 저장하는 폴더입니다.
  - `training.log`: 훈련 중 발생하는 로그를 기록하는 파일입니다.
- **README.md**: 프로젝트 설명서로, 프로젝트 개요, 실행 방법, 설치 방법, 기여 방법 등을 포함한 파일입니다.

## 설치 및 실행 방법

1. **Python 환경 설치**:

   - `requirements.txt` 또는 `environment.yml` 파일을 사용하여 필요한 라이브러리를 설치합니다.
     ```bash
     pip install -r requirements.txt
     ```
     또는 Conda 환경을 사용할 경우:
     ```bash
     conda env create -f environment.yml
     ```

2. **모델 훈련**:

   - `notebooks/model_training.ipynb`에서 모델 훈련을 시작할 수 있습니다.

3. **API 서버 실행**:

   - FastAPI 또는 Flask 앱을 실행하려면 `src/api/main.py`를 실행합니다.
     ```bash
     uvicorn src.api.main:app --reload
     ```

4. **데이터 전처리**:
   - `data/scripts/preprocess_data.py` 스크립트를 실행하여 데이터를 전처리합니다.

## 기여 방법

1. **Fork** 프로젝트
2. **기여하기**: 코드 수정 후 **Pull Request**를 제출해 주세요.
3. **Issues**: 프로젝트에 문제가 있으면 **Issues** 탭을 통해 알려 주세요.

## 라이센스

이 프로젝트는 [MIT License](LICENSE) 하에 제공됩니다.

---
