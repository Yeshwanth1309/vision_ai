import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import base64

from services.vision_service import analyze_image

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "image" not in request.files:
            return "No image uploaded"

        file = request.files["image"]

        if file.filename == "":
            return "Please select an image"

        image_bytes = file.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        result = analyze_image(image_bytes)

        return render_template(
            "result.html",
            result=result,
            image_data=image_base64,
            image_type=file.content_type
        )

    except Exception as e:
        return f"<h3>Error</h3><pre>{str(e)}</pre>", 500


if __name__ == "__main__":
    app.run(debug=True)
