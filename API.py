from flask import Flask, request
from flask_cors import CORS
from MY_modules import prepare_output_dir
from main import index_keyframes

app = Flask(__name__)
CORS(app)

@app.route("/index", methods=['POST'])
def index():
    # check the metadata if the file details and check if the file has been recieved
    if request.method == 'POST':   
        keyframes_dir = request.form['keyframes_dir'] 
        file = request.files['file_upload'] 
        if file:
            prepare_output_dir('uploads')
            file_path = f"uploads/{file.filename}"
            file.save(file_path)

        index_keyframes(file_path,keyframes_dir)
        return {"Acknowledgement":"File recieved"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)