import argparse
import os
import numpy as np
import shutil

from tqdm import tqdm
from PIL import Image
from pathlib import Path

def arg_parse():
    parser=argparse.ArgumentParser()
    
    parser.add_argument('--target_ann_dir',help='Directory which you want to process',type=str)
    parser.add_argument('--target_class_id_path',type=str)
    parser.add_argument('--output_ann_dir',help='Directory which save output',type=str)
    parser.add_argument('--img_copy',default=False,action='store_true',help='If you want image copy')
    return parser.parse_args()

def main(args):
    origin_img_dir_path=args.target_ann_dir
    origin_class_name_path=args.target_class_id_path
    
    processed_img_dir_path=args.output_ann_dir
    processed_class_name_path=str(Path(processed_img_dir_path).parent)+'/classes.txt'
    
    if not os.path.exists(processed_img_dir_path):
        os.makedirs(processed_img_dir_path)
        
    ####################################################
    '''
    Class Id File Process
    '''
    class_list=[]
    with open(origin_class_name_path,'r') as f:
        lines=f.readlines()
        for l in lines:
            class_id,class_name=l.split(',')
            line_str=str(int(class_id)) + ' ' + str(class_name)
            class_list.append(line_str)
            
    with open(processed_class_name_path,'w') as f:
        f.writelines(class_list)
    ####################################################
        
    ####################################################
    '''
    Annotation File Process
    '''
    for file in tqdm(os.listdir(origin_img_dir_path)):
        if file.endswith('.txt'):
            img_file=file.split('.')[0]+'.png'
            height,width,_=np.array(Image.open(os.path.join(origin_img_dir_path,img_file))).shape
            temp_list=[]
            with open(os.path.join(origin_img_dir_path,file),'r') as f:
                lines=f.readlines()
                for line in lines:
                    temp=''
                    line_list=line.split(' ')
                    box=[int(line_list[1]),int(line_list[2]),int(line_list[3]),int(line_list[6])]
                    size=[width,height]
                    x,y,w,h=convert(size,box)
                    temp+=str(int(float(line_list[0])))+' '+str(x)+' '+str(y)+' '+str(w)+' '+str(h)+'\n'
                    temp_list.append(temp)

            with open(os.path.join(processed_img_dir_path,file),'w') as f:
                f.writelines(temp_list)
            
            if args.img_copy:
                shutil.copy(os.path.join(origin_img_dir_path,img_file),
                            os.path.join(processed_img_dir_path,img_file))
                
def convert(size, box):
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
                
if __name__ == '__main__':
    
    args = arg_parse()
    main(args)