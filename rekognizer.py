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
import svm_service

from pymongo import MongoClient

# tweet analyzer
from tweetlyzer import tweetlyze

app = Flask(__name__)
client = MongoClient()
db = client.test_database
rekognition_resp = db.rekognition_response
twitter_resp = db.twitter_response

# app.config["UPLOAD_FOLDER"] = os.path.join ("static", "imgs")

client = boto3.client('rekognition')

@app.route ("/tweetlyzer", methods=["GET"])
def tweetlyzer_home() -> None :
    
    return render_template ("tweetlyzer_input.html")

@app.route ("/tweetlyzer", methods=["POST"])
def tweetlyzer() -> None :
    
    search_term = request.form["search_term"]
    print ("search_term: " + search_term)
    
    no_of_tweets = int(request.form["no_of_tweets"])
    print ("no of tweets: " + str(no_of_tweets))

    summary = tweetlyze (search_term, no_of_tweets)
    print ("here's the response")
    pprint (summary)
    twitter_resp.insert_one ({"SearchTerm": search_term,
                "NoOfTweets" : no_of_tweets,
                "TweetAnalysis" : summary)
    return render_template ("tweetlyzer_output.html"
                , the_search_term=search_term
                , the_no_of_tweets=no_of_tweets
                , tweet_analysis=summary)

@app.route ("/rekognizer", methods=["GET"])
def rekognizer_welcome() -> None :
    
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

    # client = boto3.client('rekognition')
    with open (file_name, "rb") as img_file:
        response = client.detect_faces (
            Image = { "Bytes" : img_file.read() }, Attributes = ["ALL"])
                                                  
    pprint (response)
    rekognition_resp.insert_one ({"File": file_name, "Analysis":response})
    return response

@app.route ("/rekognize_folder", methods=["GET"])
def rekognize_folder (folder_name="/home/vikas/Programs/rekognition/static/imgs/input") -> '[json]' :

    print ("Rekognize images in folder: " + folder_name)

    output_folder = "/home/vikas/Programs/rekognition/static/imgs/output"
    archive_folder = "/home/vikas/Programs/rekognition/static/imgs/archive"

    if not os.path.isdir (folder_name):
        return "Folder " + folder_name + " does not exist!"

    files = os.listdir (folder_name).sort()
    print ("enumerating folder ", folder_name, ": total ", len(files), " files")
    print (files)
    if len(files) == 0:
        return "Empty folder"
    
    aws_response = []
    count = 0
    for file in files:
        img_file = os.path.join (folder_name, file)
        print ("analyzing file: ", img_file)
        with open (img_file, "rb") as img:
            response = client.detect_faces (
                Image = { "Bytes" : img.read() }, Attributes = ["ALL"])
        aws_response.append (response)
        count += 1
        print ("Moving ", file, " to ", archive_folder)
        rekognition_resp.insert_one ({"File": img_file, "Analysis":response})
        os.rename(img_file, os.path.join (archive_folder, file))
        print (count, " out of ", len(files), " completed")

    output_file = os.path.join (output_folder, files[-1]+".json")
    print ("Writing image analysis to: ", output_file)
    with open (output_file, "w") as out_file:
        print (jsonify(aws_response), file=out_file)

    #pprint (aws_response)
    return jsonify(aws_response)

@app.route ("/svm/product/<product_id>")
def get_svm_product_data (product_id: str) -> 'json' :
    print ("Get data for product id " + product_id)
    return jsonify (svm_service.get_svm_data (product_id))


if __name__ == "__main__":
    app.run()
