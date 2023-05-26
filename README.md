# 데이터 합성데이터 기반 객체 탐지 AI 경진대회

## 주제
  합성 데이터를 활용한 자동차 탐지 AI 모델 개발
  
## 설명
  학습용 합성데이터를 활용하여 자동차 탐지를 수행하는 AI 모델을 개발<br>
  평가는 실제데이터를 바탕으로 진행되며, 자동차 탐지 뿐만 아니라 34가지의 자동차 세부모델까지 판별
  
## 데이터 출처
  https://drive.google.com/file/d/1fSGcTmMIaADiw6xfBITgkSYlTRqt94hy/view (ZIP파일, 25GB)
  
## 데이터 설명
  1. 학습 데이터<br>
  합성 이미지 6481장<br>
  각 이미지의 annotation 파일 6481개 (annotation 형식: class_id,x1,y1,x2,y1,x2,y2,x1,y2)<br>
  이미지 예시)<br>
  ![ex_screenshot](./fig/train1.png)
  
  2. 검증 데이터<br>
  실제 이미지 3400장<br>
  이미지 예시)<br>
  ![ex_screenshot](./fig/test1.png)
  
  3. classes.txt<br>
  총 34개의 차종에 대한 파일 (class_id,차종) 

## Project Flow
  1. 데이터 전처리<br>
    1) Object Detection에서 일반적으로 사용하는 Annotation 형식으로 맞춰줌 (ex: YOLO, COCO)<br>
    2) Data Augmentation 진행<br>
    3) 사전에 조사한 모델이 요구하는 데이터 셋 구성<br>

  2. 훈련 준비<br>
    1) 모델 환경 구성: 사전에 조사한 모델이 요구하는 가상환경 구성<br>
    2) Config 파일 구성: 모델이 학습함에 있어 필요한 Config파일들 구성<br>

  3. 훈련<br>
    1) 모델 훈련이 진행됨에 있어 도출되는 로그를 확인하며 훈련 진행도 확인<br>
  
  4. Inference 진행 및 성능 평가<br>
    1) 훈련된 모델을 통해 Detection 진행<br>
    2) Detection 결과를 제출하여 성능 점수 확인 후 Hyper Parameter 조정 진행 후 2번 부터 다시 시작<br>
