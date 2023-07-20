InternImage
======

# Installation
  1) 가상환경 구성
     ```
     conda create -n internimage python=3.7 -y
     conda activate internimage
     ```
  2) Git Clone
     ```
     git clone https://github.com/OpenGVLab/InternImage.git
     cd InternImage
     ```
  3) Install PyTorch
     PC의 설치된 CUDA 버전(CUDA 10.2 이상)에 맞춰 PyTorch 1.10.0 이상 torchvision 0.9.0 이상의 버전으로 설치
     ```
     pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113  -f https://download.pytorch.org/whl/torch_stable.html
     ```
  4) Install Another Library
     ```
     pip install -U openmim
     mim install mmcv-full==1.5.0
     pip install timm==0.6.11 mmdet==2.28.1
     pip install opencv-python termcolor yacs pyyaml scipy
     ```
  5) Compile CUDA Operators
     ```
     cd ./ops_dcnv3
     python setup.py build install
     # 정상적으로 컴파일 되었는지 테스트 진행
     python test.py 
     ```
# Prepare Dataset
  1) Dataset Structure
     ```
     Dataset
     ├── train
     |   └── image1.png ...
     ├── validation
     |   └── image10.png ...
     └── annotations
         ├── train.json
         └── valid.json
     ```
     데이터 셋 구조는 COCO 데이터 셋의 형식에 맞춰 구성<br>
     annotaions 폴더 안에 train.json과 validation.json은 각 train 데이터와 validation 데이터의 annotation 정보 함유
  2) Datatype Config 파일 생성
     가상환경이 설치된 경로 확인 후 해당 경로 내 {가상환경 경로}\Lib\site-packages\mmdet\datasets\coco.py를 참고하여 custom_data.py 작성
     ```
     class DaconDataset(CustomDataset):
       CLASSES = (데이터의 클라스 종류)
       PALETTE = (데이터의 클라스 개수에 맞게 지정)
       ...
     ```
     {가상환경 경로}\Lib\site-packages\mmdet\datasets\__init__.py 에 작성한 custom_data.py 등록
     ```
     ...
     from .custom_data import DaconDataset

     __all__ = ['DaconDataset',...]
     ```
  4) Dataset에 대한 Config 파일 생성
     InternImage/detection/configs/_base_/datasets/coco_detection.py 참고하여 custom_data_config.py 작성
     ```
     datadataset_type = '{등록한 data type}'
     data_root = '{데이터 셋 경로}'
     ...
     data = dict(
     samples_per_gpu=2,
     workers_per_gpu=2,
     train=dict(
         type=dataset_type,
         ann_file=data_root + '/annotations/train.json',
         img_prefix=data_root + '/train/',
         pipeline=train_pipeline),
     val=dict(
         type=dataset_type,
         ann_file=data_root + '/annotations/valid.json',
         img_prefix=data_root + '/valid/',
         pipeline=test_pipeline),
     test=dict(
         type=dataset_type,
         ann_file=data_root + '/annotations/valid.json',
         img_prefix=data_root + '/valid/',
         pipeline=test_pipeline))
     ...
     ```
# Prepare Train 
  1) Train Config 파일 생성
     InternImage/detection/configs/coco/dino_4scale_internimage_t_1x_coco_layer_wise_lr.py 참고하여 custom_train_config.py 작성
     ```
     _base_ = [
        '{작성한 Dataset에 대한 Config파일 경로}',
        '../_base_/default_runtime.py',
        '../_base_/schedules/schedule_2x.py',
     ]
     pretrained = 'https://huggingface.co/OpenGVLab/InternImage/resolve/main/internimage_l_22k_192to384.pth'
     ...
     model = dict(
        type='DINO',
        ...
        bbox_head=dict(
             ...
             num_classes={데이터 셋의 클라스 종류 개수},
             ...)
        ...
     ...
     data = dict(
       samples_per_gpu={batch size 결정},
       train=dict(pipeline=train_pipeline))
     ...
     ```
# Train
  Train Sytax
  ```
  python train.py {작성한 Train Config파일 경로} --work-dir {훈련 결과를 저장할 디렉토리 경로} 
  ```
     
