from flask import Flask, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)

import computer_vision
@app.route("/parse_text_from_image", methods=["POST"])
def route_parse_text_from_image():
    image = request.files["file"]
    image.save(os.path.join("public/", image.filename))
    return jsonify(computer_vision.parse_text_from_image("public/" + image.filename))

@app.route("/translate_ingredients", methods=["POST"])
def route_translate_ingredients():
    food_id = request.form["food_id"]
    language = request.form["language"]
    return jsonify(computer_vision.get_ingredients(food_id, language))

if __name__ == "__main__":
    app.run(port=5000)