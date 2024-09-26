from MY_modules import unzip, prepare_output_dir
from image_classifier import img_classification_model
from api_requests import multipart_post
from mysql_DB import insert_video_categories
from MY_modules import extract_audio
from elastic import insert_into_elastic
from ASR_model import speech_recog
import json

def index_keyframes(keyframes_zipfile_path:str,keyframes_dir:str,vid_file_name:str, mode:str):
    print("$$ Index process started")
    prepare_output_dir(keyframes_dir)    
    unzip(keyframes_zipfile_path)
    img_classification_model(keyframes_dir,vid_file_name)

    # post_response = multipart_post(url='http://127.0.0.1:5004',
    #                           file_name='keyframes_classified',
    #                           file_type='json',
    #                           file_path='keyframes_classified.json')
    if (mode == "standalone"):
        with open("keyframes_classified.json", "r") as file:
            indexed_data = json.load(file)
        return {"status":"success",
                "service_name":"Vision_Transformer",
                "video_file":vid_file_name,
                "keyframes_classified":indexed_data}
    
    insert_video_categories("keyframes_classified.json")

    # print("$$ Post response from media server: ",post_response)
    
    return {"status":"success",
            "service_name":"Vision_Transformer",
            "video_file":vid_file_name}#post_response}

def asr(filename, mode="chained"):
    audio_extract_resp = extract_audio(filename)
    print(audio_extract_resp)

    transcript = str(speech_recog(filename))

    if mode == "standalone":
        return {"filename":filename,
                "transcript":transcript}
            
    if mode == "chained":
        resp = insert_into_elastic(filename, transcript)
        return {"elastic_response": str(resp)}