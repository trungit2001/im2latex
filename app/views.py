import os

from app import app, latex_producer
from app.utils import (
    allowed_file,
    load_and_transform_image
)
from app.settings import BASE_URL
from werkzeug.utils import secure_filename
from flask import (
    request,
    redirect,
    render_template,
    abort,
    flash,
    url_for
)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def invalid_route(e):
    return render_template("page_not_found.html"), 404


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        upload_url = BASE_URL + "upload"
        return render_template("upload.html", upload_url=upload_url)

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            abort(404)

        file = request.files["file"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("predict", filename=filename))
        else:
            abort(404)
    else:
        abort(404)


@app.route("/predict/<string:filename>", methods=["GET", "POST"])
def predict(filename):
    file = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file):
        print('No such file:', filename)
        abort(404)
    else:
        image_tesor = load_and_transform_image(file)
        latex_res = latex_producer(image_tesor)

        if latex_res:
            latex = latex_res[0]
            return render_template("prediction.html", img_src="../static/images/" + filename, label=latex)
        else:
            abort(404)