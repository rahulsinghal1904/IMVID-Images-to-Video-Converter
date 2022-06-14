
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import sys
from werkzeug.utils import secure_filename
import urllib.request
from moviepy.editor import *


app = Flask(__name__)
  
UPLOAD_FOLDER = 'static/uploads/'
 
app = Flask(__name__)
app.secret_key = "image to videos"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
import cv2

def resize(img_array, align_mode):
    
    _height = len(img_array[0])
    _width = len(img_array[0][0])
    for i in range(1, len(img_array)):
        img = img_array[i]
        height = len(img)
        width = len(img[0])
        if align_mode == 'smallest':
            if height < _height:
                _height = height
            if width < _width:
                _width = width
        else:
            if height > _height:
                _height = height
            if width > _width:
                _width = width
 
    for i in range(0, len(img_array)):
        img1 = cv2.resize(img_array[i], (_width, _height), interpolation=cv2.INTER_CUBIC)
        img_array[i] = img1
 
    return img_array, (_width, _height)

def images_to_video(images, video_file):
    # make all image size is same
    img_array = []
    for i in images:
        img = cv2.imread(i)
        if img is None:
            continue
        img_array.append(img)
    img_array, size = resize(img_array, 'largest')
    fps = 0.20

    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
 

    for i in range(len(img_array)):
        out.write(img_array[i])


    out.release()



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
@app.route('/')
def upload_form():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    video_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(UPLOAD_FOLDER+filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    frames = [ImageClip(f, duration = 4) for f in file_names]
    clip = concatenate_videoclips(frames, method = "compose")
    clip.write_videofile(UPLOAD_FOLDER + 'cvideo.mp4', fps = 24)
    #images_to_video(file_names, UPLOAD_FOLDER + 'cvideo.mp4')
    print(file_names, file = sys.stderr)
    video_names.append('cvideo.mp4')
    print(video_names, file=sys.stderr)
    return render_template('index.html', filenames=video_names)
 
@app.route('/display/<filename>')
def display_video(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
  
if __name__ == "__main__":
    app.run(threaded=True)