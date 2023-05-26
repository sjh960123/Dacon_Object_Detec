import argparse
from hmac import new
import numpy as np
import os
import cv2
import random
import matplotlib.pyplot as plt
import shutil

from PIL import Image
from tqdm import tqdm
from pathlib import Path

def arg_parse():
    parser=argparse.ArgumentParser()
    
    parser.add_argument('--input_dir',help='Directory which you want to process',type=str)
    parser.add_argument('--class_path',help='Path classes.txt',type=str)
    parser.add_argument('--img_ext',default='.png',type=str,help='Image File Extension')
    parser.add_argument('--output_ann_dir',help='Directory which save output',type=str)
    parser.add_argument('--num_img',default=10,type=int,help='number of file make')
    parser.add_argument('--total',default=False,action='store_true',help='Process Total Data')
    parser.add_argument('--num_samples',default=100,type=int,help='number of sample')
    return parser.parse_args()

def nxywh2xyxy(size,box):
    height,width=size
    x,y,w,h=box
    x=x*width
    y=y*height
    w=w*width
    h=h*height
    
    x1=int(((2*x) -w)/2)
    x2=int(((2*x)+w)/2)
    y1=int(((2*y)-h)/2)
    y2=int(((2*y)+h)/2)
    return x1,y1,x2,y2

def load_img_bbox(img_path,txt_path):
    img=np.array(Image.open(img_path))
    h,w,_=img.shape
    
    bbox_list=[]
    with open(txt_path,'r') as f:
        lines=f.readlines()
        for line in lines:
            line_list=line.strip().split(' ')
            
            ann_temp=[]
            box_temp=[]
            for idx, ann in enumerate(line_list):
                if idx==0:
                    ann_temp.append(int(ann))
                else:
                    box_temp.append(float(ann))
            x1,y1,x2,y2=nxywh2xyxy((h,w),box_temp)
            box=[x1,y1,x2,y2]
            ann_temp.append(box)
            bbox_list.append(ann_temp)
    
    return img,bbox_list

def random_horizon_flip(img,p=0.5):
    if np.random.random() < p:
        img=img[:,::-1,:]
    return img

def random_resize(img,p=0.5):
    if np.random.random() < p:
        random_ratio=np.random.randint(2,5)
        h,w,_=img.shape
        img=cv2.resize(img,(int(w/random_ratio),int(h/random_ratio)))
    return img


def Image_Extract(img,ann_list):
    n_crop_img=np.random.randint(1,len(ann_list)+1)
    crop_ann_list=random.sample(ann_list,n_crop_img)
    
    crop_img_ann_list=[]
    for crop_ann in crop_ann_list:
        class_id,box=crop_ann
        
        x1,y1,x2,y2=box
        cropped_img=random_horizon_flip(img[y1:y2,x1:x2])

        # cropped_img=random_resize(cropped_img)

        crop_temp=[class_id,cropped_img]
        crop_img_ann_list.append(crop_temp)
    return crop_img_ann_list

def IoU(box1, box2):
    # box = (x1, y1, x2, y2)
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # obtain x1, y1, x2, y2 of the intersection
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # compute the width and height of the intersection
    w = max(0, x2 - x1 + 1)
    h = max(0, y2 - y1 + 1)

    inter = w * h
    iou = inter / (box1_area + box2_area - inter)
    return iou

def add_image(main_img,main_ann,crop_img_ann_list):
    main_temp=main_img.copy()
    new_ann=main_ann.copy()
    for crop_img_ann in crop_img_ann_list:
        added_class, added_img = crop_img_ann
        
        add_x1=np.random.randint(0,main_temp.shape[1]-added_img.shape[1])
        add_x2=add_x1+added_img.shape[1]

        add_y1=np.random.randint(0,main_temp.shape[0]-added_img.shape[0])
        add_y2=add_y1+added_img.shape[0]

        added_box=[add_x1,add_y1,add_x2,add_y2]
        
        iou_list=[]
        for ann in new_ann:
            _,main_box=ann

            iou=IoU(main_box,added_box)
            iou_list.append(iou)
        
        if sum(iou_list)==0:
            main_temp[add_y1:add_y2,add_x1:add_x2]=added_img
            new_ann.append([added_class,added_box])
                

    return main_temp,new_ann

def xyxy2nxywh(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[2])/2.0
    y = (box[1] + box[3])/2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def save_file(main_temp,main_ann,output_dir,file_name):
    height,width,_=main_temp.shape
    
    ann_list=[]
    for ann in main_ann:
        class_id,box=ann
        x,y,w,h=xyxy2nxywh([width,height],box)
        ann_str=str(class_id)+' '+str(x)+' '+str(y)+' '+str(w)+' '+str(h)+'\n'
        ann_list.append(ann_str)
        
    plt.imsave(os.path.join(output_dir,file_name+'.jpg'),main_temp)
    with open (os.path.join(output_dir,file_name+'.txt'),'w') as f:
        f.writelines(ann_list)

def main(args):
    
    file_list=[]
    for file in os.listdir(args.input_dir):
        file_name=file.split('.')[0]
        if file_name in file_list:
            pass
        else:
            file_list.append(file_name)
    
    
    if not args.total:
        process_list=random.sample(file_list,args.num_samples)
    else:
        process_list=file_list

    if not os.path.exists(args.output_ann_dir):
        os.makedirs(args.output_ann_dir)

    ann_dir=os.path.join(args.output_ann_dir,'result')
    if not os.path.exists(ann_dir):
        os.makedirs(ann_dir)

    shutil.copy(args.class_path,args.output_ann_dir)

    for file in tqdm(process_list):
        for i in range(args.num_img):
            main_img_path=os.path.join(args.input_dir,file+args.img_ext)
            main_ann_path=os.path.join(args.input_dir,file+'.txt')
            
            main_img,main_ann=load_img_bbox(main_img_path,main_ann_path)
            # print(len(main_ann))
            sample_list=random.sample(process_list,args.num_img)
            
            save_file_name=file+'_'+str(i)
            while True:
                for sample in sample_list:
                    
                    sample_img_path=os.path.join(args.input_dir,sample+args.img_ext)
                    sample_ann_path=os.path.join(args.input_dir,sample+'.txt')

                    sample_img,sample_ann=load_img_bbox(sample_img_path,sample_ann_path)
                    
                    crop_img_ann_list=Image_Extract(sample_img,sample_ann)

                    new_img,new_ann=add_image(main_img,main_ann,crop_img_ann_list)
                    
                if len(new_ann)>len(main_ann):
                    save_file(new_img,new_ann,ann_dir,save_file_name)  
                    print(f'Save Image {save_file_name}')
                    break
                
                else:
                    continue
 
if __name__ == '__main__':
    
    args = arg_parse()
    main(args)