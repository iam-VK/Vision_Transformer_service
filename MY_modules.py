import glob
import re
import json
import os
from zipfile import ZipFile 

def vidName_from_path(vid_dir_path:str="Videos"):
    '''Extract only video name from the dir of videos
    args:
    path to Videos directory  
    
    output:
    returns a list of video file names
    '''
    vid_files = glob.glob(vid_dir_path+'/*')
    return [name.replace(".mp4","").replace(vid_dir_path,"").replace("\\","").replace("/","") for name in vid_files]

def unzip(zipped_file):
    with ZipFile(zipped_file, 'r') as zip_ref:
        zip_ref.extractall(".")

def prepare_output_dir(output_path:str):
    isExist = os.path.exists(output_path)
    if isExist:
        old_files = glob.glob(output_path+'/*')
        for f in old_files:
            os.remove(f)
    else:
        os.makedirs(output_path)
    
    return output_path

def imgPath_To_List (keyframes_dir_path:str="key_frames"):
  '''Creates relative path 
  args:
  directory with keyframe images

  output:
  returns a list of relative path to the images
  '''
  key_frames = glob.glob(keyframes_dir_path+"/*")
  return key_frames

def category_To_category_id(category_name:str):
    with open("ImageNet_classes.json", mode='r') as f:
        imageNet_classes = json.load(f)
        category_id = list(imageNet_classes.keys())[list(imageNet_classes.values()).index(category_name)]
        return category_id

def json_parser(input_data,src_file:str,img_dir:str="key_frames", output_file_name:str="keyframes_classified"):
    lines = input_data

    old_files = glob.glob(img_dir+'/*')
    frame_ids = [str(re.findall("frame_[0-9]*",name)).replace("['","").replace("']","") for name in old_files]

    data = {"src_file":src_file, 
            "keyframes_classified": {}}

    for i, line in enumerate(lines):
        items = [item.strip() for item in line.split(',')]
        category_id = category_To_category_id(line)
        data["keyframes_classified"][i] = {"frame_id":frame_ids[i],
                   "category_id":category_id,
                   "category":items}
        
    with open(output_file_name+".json", "w") as file:
        json.dump(data, file)
