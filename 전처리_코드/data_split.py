import argparse
import os
import random 
import numpy as np
import shutil

from tqdm import tqdm

def arg_parse():
    parser=argparse.ArgumentParser()
    
    parser.add_argument('--input_dir',help='Directory which you want to process',type=str)
    parser.add_argument('--output_dir',help='Directory which save output',type=str)
    parser.add_argument('--ratio',default=0.3,type=float,help='Train Valid Split Ratio(test_size)')
    return parser.parse_args()

def main(args):
    data_list=[]
    for data in os.listdir(args.input_dir):
        data_name=data.split('.')[0]
        if data_name not in data_list:
            data_list.append(data_name)
        else:
            pass
        
    train_data_list=random.sample(data_list,int(len(data_list)*(1-args.ratio)))
    valid_data_list=[file for file in data_list if file not in train_data_list]
    
    train_dir=os.path.join(args.output_dir,'train')
    valid_dir=os.path.join(args.output_dir,'valid')
    
    os.makedirs(train_dir,exist_ok=True)
    os.makedirs(valid_dir,exist_ok=True)
    
    for data in tqdm(train_data_list):
        
        shutil.copy(os.path.join(args.input_dir,data+'.png'),
                    os.path.join(train_dir,data+'.jpg'))
        
        shutil.copy(os.path.join(args.input_dir,data+'.txt'),
                    os.path.join(train_dir,data+'.txt'))
        
    for data in tqdm(valid_data_list):
        
        shutil.copy(os.path.join(args.input_dir,data+'.png'),
                    os.path.join(valid_dir,data+'.jpg'))
        
        shutil.copy(os.path.join(args.input_dir,data+'.txt'),
                    os.path.join(valid_dir,data+'.txt'))
        
if __name__ == '__main__':
    
    args = arg_parse()
    main(args)