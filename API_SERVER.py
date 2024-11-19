from flask import Flask, request
from flask_cors import CORS
from MY_modules import prepare_output_dir
from main import index_keyframes

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST','GET'])
def service_status():
    return {
            "status": 'Alive',
            "endpoints": {
                "/index": {
                    "method": "POST",
                    "parameters": {
                        "form_data": ["dir", "vid_name"],
                        "file_upload": "video file",
                        "mode":"standalone, default db"
                    }
                }
            }
        }

@app.route("/video-index", methods=['POST'])
def index():
    # TODO: check the metadata for file details and check if the file has been recieved
    if request.method == 'POST':
        keyframes_dir = request.form['dir'] 
        vid_file_name = request.form['vid_name']
        file = request.files['file_upload']
        mode = request.form.get('mode',"chained") # other mode:standalone, default mode:db

        if file:
            prepare_output_dir('uploads')
            filename = file.filename
            file_path = f"uploads/{filename}"
            file.save(file_path)

        resp_vision = index_keyframes(file_path,keyframes_dir,vid_file_name, mode)
        return {"Acknowledgement":"File recieved",
                "ViT-Result":resp_vision}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, use_reloader = True)