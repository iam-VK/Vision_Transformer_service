from elasticsearch import Elasticsearch
from mysql_DB import video_To_video_id
from MY_modules import file_name_extract

client = Elasticsearch(
  "https://localhost:9200/",
  api_key="N2l1TUlwSUJTMWxfTmtUOGlpR1M6cThDOVNGTEJUNXVwZ2VzY2t2OG4tdw==",
  verify_certs=False,
  ssl_show_warn=False
)

def insert_into_elastic(filename, transcription):
    _, filename_without_extension = file_name_extract(filename)
    video_id = video_To_video_id(filename_without_extension)
    doc = {
        "file_name":filename,
        "video_id":video_id,
        "transcription":transcription
    }

    resp = client.index(index="transcription-index", document=doc, id=video_id)
    print("response from elastic: ",resp)
    return resp