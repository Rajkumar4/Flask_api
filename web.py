import os
from flask import flash, Flask, render_template, redirect
from flask_limiter import Limiter
from flask import request
from werkzeug.utils import secure_filename
import logging


app = Flask(__name__)
app.secret_key = "secret-key"
path = ".\store"
app.config["path"] = path
app.config["Max_Content_length"] = 1024 * 1024 * 10
limiter = Limiter(app, global_limits=["5 per minute"])
imageExt = {"jpg", "png", "bmp", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in imageExt


@app.route("/")
def web():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method != "POST":
        flash("Use appropriate method")
        return "method is worng"
    logging.error(request.files)
    if "file" not in request.files:
        flash("File is not persent")
        return "Error found"
    
    file = request.files['file']
    if file.filename == "":
        flash("No file is selected")
        return "Erorr found in name of file"
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["path"], filename))
        return "file " + filename + " is uploaded"
    else:
        return "Choose valid file"


if (__name__) == "__main__":
    app.run(host="localhost", port="5000", debug=True)

