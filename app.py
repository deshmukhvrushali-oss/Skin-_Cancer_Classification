import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from predict import predict_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 🔹 Login Page
@app.route("/")
def login():
    return render_template("login.html")


# 🔹 Upload Page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload.html")


# 🔹 Result Page
@app.route("/result", methods=["POST"])
def result():

    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    city = request.form.get("city")

    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No selected file"

    if not allowed_file(file.filename):
        return "Invalid file type"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    prediction, confidence = predict_image(filepath)

    # Risk Logic
    if prediction.lower() == "melanoma":
        risk = "High Risk"
        message = "⚠ Immediate dermatologist consultation recommended."
        color = "red"

    elif prediction.lower() == "bkl":
        risk = "Moderate Risk"
        message = "Clinical examination suggested."
        color = "orange"

    else:
        risk = "Low Risk"
        message = "Regular monitoring recommended."
        color = "green"

    return render_template(
        "result.html",
        name=name,
        age=age,
        gender=gender,
        city=city,
        prediction=prediction.upper(),
        confidence=round(confidence * 100, 2),
        risk=risk,
        message=message,
        color=color,
        image_path=filepath,
        accuracy=80,
        successful_cases="12,540+",
        expert_doctors="25+",
        cities_covered="18+"
    )


if __name__ == "__main__":
    app.run(debug=True)