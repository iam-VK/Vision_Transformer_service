from MY_modules import unzip
from image_classifier import img_classification_model
from api_requests import multipart_post

def index_keyframes(keyframes_zipfile:str,keyframes_dir):
    print("$$ Index process started")
    unzip(keyframes_zipfile)
    img_classification_model(keyframes_zipfile)

    # post_response = multipart_post(url='http://127.0.0.1:5003',
    #                           file_name='key_frames_classified',
    #                           file_type='json',
    #                           file_path='keyframes_classified.json')
    
    return {"post_response":"ok"}#post_response}