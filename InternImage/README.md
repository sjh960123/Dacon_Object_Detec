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
     
