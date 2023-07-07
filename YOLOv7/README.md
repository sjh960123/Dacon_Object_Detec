YOLOv7
======

# Installation
  1) 가상환경 구성:
      ```
      conda create -n yolov7 python=3.7.3 -y
      ```
  2) Git Clone:
      ```
      git clone https://github.com/WongKinYiu/yolov7
      cd yolov7
      ```
  3) Install Pytorch 
      PC의 설치된 CUDA 버전에 맞춰 torch 버전 1.7.0 이상을 설치 하되 1.12.0은 안됨<br>
      (본인 PC의 경우 CUDA 11.1과 CUDA 11.3이 설치 되어 있어 torch 1.9.1로 진행):
      ```
      pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
      ```
  4) Install Another Library
      requirements.txt 에서 torch, torchvision 항목 제거 후 다른 라이브러리 설치 진행( 3)에서 torch 설치 진행 )
      ```
      pip install -r requirements.txt
      ```
# Prepare Dataset
  1) Dataset Structure
     ```
     Dataset
     ├── train
     |   ├── images
     |       └── image1.png ...
     |   └── labels
     |       └── image1.txt ...
     └── validation
         ├── images
         |   └── image10.png ...
         └── labels
             └── image10.txt ...
     ```
  2) Create YAML File
     ```
     train: {train directory path}
     val: {validation directory path}

     nc: {number of classes}

     names:[classes of dataset]
     ```
# How to Train YOLOv7
  1) Download Pretrained Model
     https://github.com/WongKinYiu/yolov7/releases/tag/v0.1
