from flask import Flask,url_for,render_template,request, redirect,flash
import cv2,os

app =  Flask(__name__)

app.secret_key = "secret key"

#Upload directory 
UPLOAD_FOLDER = 'D:\rahul.devadasan\flask_tutorial\imagesave'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Opening page runner
@app.route("/")
def runner():
	return render_template("index.html")
    
#image capture using webcam
@app.route("/imagecap", methods=['GET','POST'])
def imagecapture():
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while(result):
        ret,frame = videoCaptureObject.read()
        
        cv2.imwrite("NewImage.png",frame)
        result = False
        videoCaptureObject.release()
        cv2.destroyAllWindows()
        
    return render_template('index.html',captured_image = frame)


#upload image

#the issue is here. 	
@app.route("/", methods=['GET','POST'])
def uploadimage():
    if request.method == "POST":
         if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
         file = request.files['file']
         if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed')
            #cv2.imwrite("NewImage.png",file)
            return render_template('index.html', filename=filename)
         else:
            flash('Allowed image types are -> png, jpg, jpeg')
            return redirect(request.url)

      
            
    

if __name__ == "__main__":
	app.run()
	
	