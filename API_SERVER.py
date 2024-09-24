from flask import Flask, request
from flask_cors import CORS
from MY_modules import prepare_output_dir, extract_audio
from main import index_keyframes
from ASR_model import speech_recog
# 908756
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
                        "file_upload": "video file"
                    }
                }
            }
        }

@app.route("/index", methods=['POST'])
def index():
    # check the metadata for file details and check if the file has been recieved
    if request.method == 'POST':
        keyframes_dir = request.form['dir'] 
        vid_file_name = request.form['vid_name']
        file = request.files['file_upload'] 
        mode = request.form.get('mode',"chained") # other mode:standalone, default mode:chained

        if file:
            prepare_output_dir('uploads')
            file_path = f"uploads/{file.filename}"
            file.save(file_path)

        response = index_keyframes(file_path,keyframes_dir,vid_file_name, mode)
        return {"Acknowledgement":"File recieved","Result":response}

@app.route("/speech-recog", methods=['POST'])
def speech_model():
    # check the metadata for file details and check if the file has been recieved
    if request.method == 'POST':
        file = request.files['file_upload']
        mode = request.form.get('mode',"chained") # other mode:standalone, default mode:chained

        if file:
            prepare_output_dir('uploads')
            filename = file.filename
            file_path = f"uploads/{filename}"
            file.save(file_path)

            return_message = extract_audio(filename)
            print(return_message)

            transcript = speech_recog(filename)

            if mode == "standalone":
                return {"filename":filename,
                        "transcript":transcript}
            

        # //response = index_keyframes(file_path,vid_file_name, mode)
        # //return {"Acknowledgement":"File recieved","Result":response}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, use_reloader = True)