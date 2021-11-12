from flask import Flask, make_response, request, redirect, render_template
from werkzeug.utils import secure_filename
import PDF_To_Booklet as PTB
import os

app = Flask(__name__)

flask_dir = os.path.dirname(__file__)
pdf_dir= os.path.join(flask_dir,'static','pdf')

@app.route('/')
def index_html():
    return render_template('index.html',
            template_folder=os.path.join(flask_dir,'templates'),
            static_folder=os.path.join(flask_dir,'static'))

@app.route('/upload', methods=['POST'])
def save_file():
    file = request.files['file']

    upload_path = os.path.join(pdf_dir,file.filename)
    thumb_path = os.path.join(pdf_dir,'thumb_'+file.filename)
    booklet_path = os.path.join(pdf_dir,'booklet_'+file.filename)

    if(os.path.isfile(upload_path)):
        os.remove(upload_path)
    if(os.path.isfile(thumb_path)):
        os.remove(thumb_path)    
    if(os.path.isfile(booklet_path)):
        os.remove(booklet_path)

    file.save(upload_path)
    PTB.Make_Thumb(upload_path,thumb_path)
    PTB.Make_Booklet(upload_path,booklet_path)

    #PDFの1ページ目をサムネイルとして送りかえす
    response = make_response()
    response.data = open(thumb_path,"rb").read()
    response.mimetype = "application/pdf"
  
    return response

@app.route('/download', methods=['POST'])
def send_booklet():
    filename = request.form['filename']
    sendfile_path = os.path.join(pdf_dir,filename)
    
    response = make_response()
    response.data = open(sendfile_path,"rb").read()
    response.mimetype = "application/pdf"

    return response

@app.route('/refresh',methods=['POST'])
def refresh_file():
    filename = request.form['filename']

    upload_path = os.path.join(pdf_dir,filename)
    thumb_path = os.path.join(pdf_dir,'thumb_'+filename)
    booklet_path = os.path.join(pdf_dir,'booklet_'+filename)

    if(os.path.isfile(upload_path)):
        os.remove(upload_path)
    if(os.path.isfile(thumb_path)):
        os.remove(thumb_path)    
    if(os.path.isfile(booklet_path)):
        os.remove(booklet_path)

    return redirect("/")
    
if __name__ == '__main__':
    app.run(debug=True)