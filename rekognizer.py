#!/usr/bin/python3

# AWS Libraries & Functions
import base64
import boto3
from pprint import pprint

# Flask Libraries & Functons
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

# File handling
import os

app = Flask(__name__)
# app.config["UPLOAD_FOLDER"] = os.path.join ("static", "imgs")

@app.route ("/")
@app.route ("/rekognizer", methods=["GET"])
def welcome() -> None :
    
    return render_template ("rekognizer_input.html")


@app.route ("/rekognizer", methods=["POST"])
def rekognizer () -> 'json' :

    # file_name = os.path.join (app.config["UPLOAD_FOLDER"], request.form["file_name"])
    file_name = "static/imgs/" + request.form["file_name"]
    print ("file_name: " + file_name)
    return render_template ("rekognizer_output.html",
        usr_img=file_name, facial_analysis=rekognize (file_name))


def rekognize (file_name: str) -> 'json' :

    print ("Rekognize image: " + file_name)

    if not os.path.isfile (file_name):
        return "File " + file_name + " not found!"

    client = boto3.client('rekognition')
    with open (file_name, "rb") as img_file:
        response = client.detect_faces (
            Image = { "Bytes" : img_file.read() }, Attributes = ["ALL"])
                                                  
    pprint (response)
    return response


if __name__ == "__main__":
    app.run(debug=True)
