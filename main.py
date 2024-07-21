from MY_modules import unzip, prepare_output_dir
from image_classifier import img_classification_model
from api_requests import multipart_post
from mysql_DB import insert_video_categories

def index_keyframes(keyframes_zipfile:str,keyframes_dir:str,vid_file_name:str):
    print("$$ Index process started")
    prepare_output_dir(keyframes_dir)    
    unzip(keyframes_zipfile)
    img_classification_model(keyframes_zipfile,vid_file_name)

    post_response = multipart_post(url='http://127.0.0.1:5004',
                              file_name='key_frames_classified',
                              file_type='json',
                              file_path='keyframes_classified.json')
    
    insert_video_categories("keyframes_classified.json")

    print("$$ Post response from media server: ",post_response)
    
    return {"status":"success",
            "service_name":"Vision_Transformer"}#post_response}