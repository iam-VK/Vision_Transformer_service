import requests

def multipart_post(url:str,file_name:str,file_type:str,file_path:str):
    data = {'file_name': file_name,
            'file_type': file_type}

    files = {'file_upload': open(file_path, 'rb')}

    response = requests.post(url, data=data, files=files)

    return response
