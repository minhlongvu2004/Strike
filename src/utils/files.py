"""
Filename: files.py
Author: Minh Long Vu
Date: 2026-07-30
Description: This script perform operations related to file such as re-index or split train,val,test...
"""

__author__ = "Minh Long Vu"
__license__ = "GPL"
__email__ = "minhlongvu626@gmail.com"
__status__ = "Prototype"

import os
from os import listdir
import shutil
from sklearn.model_selection import train_test_split


def index_files(src_dir, dest_dir, start = 1, step = 1):
    """
    Summary:
        this function simply rename all the files in a folder based on the index integer

    Args:
        src_dir: str
            The source directory of files
        dest_dir: str
            The destination directory of files
        start: int, optional, default to 1
            The start of reindex files
        step: int,optional, default to 1
            The step for reindex. Example 1,2,3 for step 1 or 1,3,5 for step 2
            
    Return:
        None
    """
    
    src_files = list()
    for file in listdir(src_dir):
        # only take the name not extension
        src_files.append(file)
        print(file)
    counter = start
    for fl in src_files:
        
        
        file_extension = fl.split(".")[1]
        new_name = f"{counter}.{file_extension}"
        
        fl_dest = f"{dest_dir}/{new_name}"
        fl_src = f"{src_dir}/{fl}"
        print(fl)
        shutil.copyfile(fl_src, fl_dest)
        counter = counter + step


def split_data(images_dir,labels_dir, percent_val=0.15,percent_test=0.15):
    """
    Summary:
        This split the data into train, val, and test folders. Each contain images and labels folders
        It assume that the label files has the same name as images files Example: img1.jpg and img1.txt

    Args:
        images_src: str
            the source of the images
        labels_src: str
            the source of the labels
        percent_val: float, optional, default to 0.15
            the percentage of validation part
        percent_test: float, optional, default to 0.15
            the percentage of test part
            
    Return:
        list[str],list[str],list[str],list[str],list[str],list[str]:
            3 images and 3 labels subsets for train, val, and test, respectively
    """
    
    
    images = list()
    labels = list()
    for img in listdir(images_dir):
        # only take the name not extension
        images.append(img)
    for label in listdir(labels_dir):
        
        labels.append(label)

    '''
    we will perform two splits
    First split of images: train_val and test parts
    Second split of train_val: train and val
    First split we only specify the train_val with 80 but
    what is the parameter for second split?
    
    Assume that N is the total rows where train,val, and test 
    are the parts with rows corresponding to percentage of total rows
    train + val + test = N
    Where
    (1) train = 0.7N, val = 0.15N and test = 0.15N
    After first split where we extract the test portion
    we have
    train + val = 0.85N
    The question is that how much percentage of these 85N we need to take
    so that it could be equal with the inital percentage of total rows. 
    We call those portions x and y for train and val, respectively
    (2) val = x * 85N, val = y * 15N
    From (1) and (2) we have
    val = y * 0.85N= 0.15N => x = 0.15 / 0.85 ~~ 0,1764 ~~ 0,18
    '''
    
    # First split
    train_val_images, test_images, train_val_labels, test_labels = train_test_split(
    images, labels, 
    test_size=percent_test, 
    random_state=42
    )
    val_size = percent_val / (1 - percent_test)
    train_images, val_images, train_labels, val_labels  = train_test_split(
    train_val_images, train_val_labels, 
    test_size= val_size, 
    random_state=42
    )
    return train_images, val_images, test_images, train_labels, val_labels, test_labels

def copy_files_to_dest(src_dir, dest_dir, src_files):
    
    """
    Summary:
        copy selected files in a directory to a locatio

    Args:
        src_dir: str
            the source directory contains all the files
        dest_dir: str
            the destination directory
        src_files: list[str] 
            the selected files in that directory 
            
    Return:
        None
    """
    
    # there might be mess up between jpg and png 
    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
    for fl in src_files:
        fl_dest = f"{dest_dir}\\{fl}"
        fl_src = f"{src_dir}\\{fl}"
        shutil.copyfile(fl_src, fl_dest)

def copy_images_labels_to_dest(images_dir,
                               labels_dir, 
                               dest, 
                               percent_val = 0.15,
                               percent_test = 0.15):
    """
    Summary:
    this application will split the data into the train format
    where it include train,val, and test inside data directory. 
    Each train,val,and test itself contains images and labels folders

    Args:
        images_dir: str
            the path to the images folder
        labels_dir: str
            the path to the labels folder
        dest: str
            the destination where we put the YOLO formated daata
        percent_val: float, optional, default to 0.15
            the percentage of validation part
        percent_test: float, optional, default to 0.15
            the percentage of test part
            
    Return:
        None
    """
    
    
    train_images, val_images, test_images, train_labels, val_labels, test_labels\
        = split_data(images_dir, labels_dir, percent_val, percent_test)
    train_images_dir = dest + "data/train/images/"
    train_labels_dir = dest + "data/train/labels/"
    
    val_images_dir = dest + "data/val/images/"
    val_labels_dir = dest + "data/val/labels/"
    
    test_images_dir = dest + "data/test/images/"
    test_labels_dir = dest + "data/test/labels/"
    
    copy_files_to_dest(images_dir, train_images_dir, train_images)
    copy_files_to_dest(labels_dir, train_labels_dir, train_labels)

    copy_files_to_dest(images_dir, val_images_dir, val_images)
    copy_files_to_dest(labels_dir, val_labels_dir, val_labels)
    
    copy_files_to_dest(images_dir, test_images_dir, test_images)
    copy_files_to_dest(labels_dir, test_labels_dir, test_labels)


if __name__ == "__main__":
    images_dir = r"images"
    labels_dir = r"labels"

    copy_images_labels_to_dest(images_dir,labels_dir,"./")