from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import PDF_To_Booklet as PTB
import os

app = Flask(__name__)

pdf_dir = os.path.dirname(__file__)
upload_path= os.path.join(pdf_dir,'static','pdf','uploaded.pdf')
pdf_path = os.path.join(pdf_dir,'static','pdf','booklet.pdf')

@app.route('/')
def index_html():
    return render_template('index.html',
            template_folder='./templates/',
            static_folder='./static/')

@app.route('/upload', methods=['POST'])
def save_file():
    file = request.files['file']




    if(os.path.isfile(upload_path)):
        os.remove(upload_path)
    file.save(upload_path)

    PTB.Make_Booklet(upload_path,pdf_path)
    return redirect("/")

@app.route('/delete')
def delete_file():
    if(os.path.isfile(upload_path)):
        os.remove(upload_path)

    if(os.path.isfile(pdf_path)):
        os.remove(pdf_path)

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)