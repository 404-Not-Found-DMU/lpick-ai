# LP 앨범 이미지 분류 AI 프로젝트

이 프로젝트는 LP 앨범의 **앞면, 뒤면, 속지, LP판(디스크)** 이미지를 각각 분류하는 AI 모델을 개발하고, 서비스까지 배포하는 실무형 워크플로우를 따릅니다.

---

## 1. 프로젝트 워크플로우

1. **데이터 준비 및 전처리**
   - 데이터 수집, 정제, 라벨링(앞면, 뒤면, 속지, LP판)
   - 데이터 분할(train/val/test), 증강, 품질 검수
2. **실험/학습 환경 세팅**
   - 환경 관리(requirements.txt, environment.yml)
   - 실험 관리 도구(MLflow, W&B, TensorBoard 등) 도입
   - 코드 구조화(데이터, 모델, 학습, 평가, 유틸 등 모듈화)
3. **모델 설계 및 학습**
   - 카테고리별(앞면, 뒤면, 속지, LP판) 독립 모델 설계 및 학습
   - 하이퍼파라미터 튜닝, 실험 자동화
   - 학습 진행률, 정확도 등 로깅 및 체크포인트 저장
4. **평가 및 검증**
   - 다양한 지표(정확도, F1, Confusion Matrix 등)로 성능 평가
   - 실험 결과 자동 기록 및 비교
5. **모델 배포 및 서비스화**
   - 추론 API(FastAPI, Flask 등) 설계
   - 모델 서빙(Docker, ONNX, GPU/CPU 선택)
   - 모니터링, 롤백, 보안 등 운영 전략
6. **문서화 및 자동화**
   - 코드/실험/운영 문서화
   - 실험 및 배포 자동화(CI/CD)

---

## 2. 폴더/코드 구조 (정리됨)

```
lpick-ai/
  data/                         # 데이터 관련
    raw/                        # 원본 데이터
      discogs/                  # Discogs 앨범 이미지 (장르별)
    processed/                  # 전처리된 데이터
      labeled/                  # 라벨링된 데이터 (front/back/inner/disk)
      dataset/                  # 학습용 데이터셋 (train/val/test)
      annotations/              # YOLO 어노테이션 파일
    scripts/                    # 데이터 처리 스크립트
      download_discogs_albums.py
      prepare_labeled_data.py
      preprocess_data.py

  models/                       # 모델 관련
    model_architectures/        # 모델 아키텍처
      clip_model.py
      resnet_model.py
    saved_models/               # 학습된 모델
      lp_classifier/
        best_model.pth
        training_history.json
        confusion_matrix.png
    scripts/                    # 모델 학습/평가 스크립트
      train_lp_classifier.py
      train_model.py
      evaluate_model.py
    utils/
      image_utils.py

  tools/                        # 개발 도구들
    labeling/                   # 라벨링 도구
      web_labeling.py           # 웹 기반 카테고리 라벨링
      interactive_labeling.py   # 콘솔 기반 라벨링
      bbox_labeling_server.py   # 바운딩 박스 라벨링 서버
    analysis/                   # 분석 도구
      test_training_results.py  # 학습 결과 분석

  scripts/                      # 실행 스크립트
    run_labeling.py             # 라벨링 도구 실행
    run_bbox_labeling.py        # 바운딩 박스 라벨링 실행
    run_full_pipeline.py        # 전체 파이프라인 실행

  src/                          # 소스 코드
    api/
      main.py
      inference.py
      search.py
    data_loader/
      image_loader.py
      text_loader.py
    models/
      clip_model.py
      ocr_model.py
      resnet_model.py
    utils/
      cosine_similarity.py
      ocr_utils.py
    visualization/
      plot_results.py

  templates/                    # HTML 템플릿
    labeling.html               # 카테고리 라벨링 UI
    bbox_labeling.html          # 바운딩 박스 라벨링 UI

  experiments/                  # 실험 결과
    front/
    back/
    inner/
    disk/

  tests/                        # 테스트
    test_data/
    test_models/
    test_api/

  config/                       # 설정 파일
    config.yaml
    logging.yaml

  notebooks/                    # Jupyter 노트북
    EDA.ipynb
    model_training.ipynb

  logs/                         # 로그 파일

  Dockerfile
  requirements.txt
  environment.yml
  README.md
  FOLDER_STRUCTURE.md
```

---

## 3. 실무에서 신경 써야 할 주요 고려사항

- **데이터 품질/드리프트 감지**: 데이터 분포 변화, 라벨 오류, 증강 부작용 등 주기적 검수
- **실험 재현성**: 랜덤시드 고정, 환경/코드/데이터/모델 버전 동기화
- **모델 성능과 속도의 Trade-off**: 실제 서비스 환경에 맞는 최적화(경량화, 속도, 정확도)
- **운영/배포 자동화**: CI/CD, 롤백, 모니터링, 장애 대응, API 보안
- **비용/자원 관리**: GPU/서버/스토리지 모니터링, 불필요 리소스 자동 종료
- **윤리/법적 이슈**: 저작권, 개인정보 보호, 라이선스 준수
- **사용자 경험(UX)**: 예측 실패 시 안내, 응답 속도, 오류 메시지 등
- **장기적 유지보수**: 기술 부채 관리, 문서화, 협업 프로세스

---

## 4. 업그레이드/재학습 및 버전 관리

- 데이터/모델/코드/실험 결과를 분리·버전 관리
- 실험 관리 도구로 어떤 조건에서 학습했는지 기록
- 체크포인트/저장된 모델로 파인튜닝, 재학습, 롤백 가능
- 새 데이터/모델이 생겨도 쉽게 업그레이드 및 서비스 반영

---

## 5. 카테고리별 독립 학습 구조

- **앞면, 뒤면, 속지, LP판(디스크)** 각각을 별도의 데이터셋과 모델로 독립적으로 학습
- 각 카테고리에 최적화된 모델 설계/튜닝 가능
- 추후 한 카테고리만 업그레이드/재학습/교체도 쉬움
- 폴더/실험/모델 파일도 카테고리별로 분리 관리

---

## 6. 실무 팁

- 실험/운영 자동화, 모니터링, 문서화는 “처음부터” 설계에 반영
- 데이터/모델/코드/실험 결과의 “버전 동기화” 필수
- 장애/이상 상황에 대한 “대응 매뉴얼” 준비
- “협업”과 “장기 유지보수”를 고려한 구조 설계

---

## 7. 라벨링 도구 사용법

### 7.1 기본 라벨링 도구 (카테고리 분류)

LP 앨범 이미지를 앞면, 뒤면, 속지, LP판으로 분류하는 도구입니다.

```bash
# 웹 기반 라벨링 도구 실행
python tools/labeling/web_labeling.py --data_dir data/raw/discogs --output_dir data/processed/labeled --port 5000

# 또는 실행 스크립트 사용
python scripts/run_labeling.py

# 콘솔 기반 라벨링 도구 실행
python tools/labeling/interactive_labeling.py --data_dir data/raw/discogs --output_dir data/processed/labeled
```

**웹 라벨링 도구 특징:**

- 브라우저에서 이미지를 보면서 직관적으로 라벨링
- 키보드 단축키 지원 (1:앞면, 2:뒤면, 3:속지, 4:LP판, s:건너뛰기)
- 진행상황 자동 저장 및 복원
- 이미지 정보 표시 (크기, 모드 등)

### 7.2 바운딩 박스 라벨링 도구 (객체 검출용)

labelImg 스타일의 바운딩 박스 라벨링 도구입니다. YOLO 형식으로 어노테이션을 저장합니다.

```bash
# 바운딩 박스 라벨링 도구 실행
python scripts/run_bbox_labeling.py

# 또는 직접 실행
python tools/labeling/bbox_labeling_server.py --data_dir data/raw/discogs --output_dir data/processed --port 5001
```

**바운딩 박스 라벨링 도구 특징:**

- 마우스 드래그로 바운딩 박스 생성
- 4가지 라벨 지원 (앞면, 뒤면, 속지, LP판)
- YOLO 형식 어노테이션 파일 자동 생성
- 키보드 단축키 지원:
  - `1-4`: 라벨 선택
  - `Ctrl+S`: 저장
  - `Delete`: 선택된 박스 삭제
  - `Space`: 다음 이미지
  - `Backspace`: 이전 이미지

**출력 형식:**

- 어노테이션 파일: `data/processed/annotations/장르/이미지명.txt`
- YOLO 형식: `class_id x_center y_center width height` (상대 좌표)

### 7.3 라벨링 도구 비교

| 도구               | 용도        | 입력   | 출력             | 특징                |
| ------------------ | ----------- | ------ | ---------------- | ------------------- |
| 웹 라벨링          | 이미지 분류 | 이미지 | 카테고리 라벨    | 전체 이미지 분류    |
| 바운딩 박스 라벨링 | 객체 검출   | 이미지 | 바운딩 박스 좌표 | 이미지 내 객체 위치 |

---

## 8. 참고 및 문의

- 각 단계별 코드/자동화/실험 관리/배포 등 구체적 예시가 필요하면 언제든 문의하세요.
