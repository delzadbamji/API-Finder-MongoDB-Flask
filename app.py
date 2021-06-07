'''
This is the server for the application.
Author: Delzad Bamji
'''

from flask import Flask, render_template, request, redirect, g

import shelve
from flask_restful import Resource, Api, reqparse
import sqlite3
import requests
import pandas as pd
import json
import configparser
import mongo_query

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    apitype = ""
    category = ""
    protocol = ""
    APIname = ""
    label=""
    # rating=""
    # sqlstring = ""
    # endpoint_info={}
    querying=""
    # if post method is called after form submission
    if request.method == "POST":
        print("FORM DATA RECEIVED IN POST METHOD")


# /////////////////////////
#         print(request.form)

        if "submitButtonGet" in request.form:
            apitype = "API"
            print("In API: ")

            # print(request.form["title1"])

            if 'title1' in request.form:
                title = request.form['title1']
            else:
                title = ""

            if request.form['rating1']:
                rating = request.form["rating1"]
                ratingDrop = request.form["rating1-drop"]
            else:
                rating = ""
                ratingDrop = request.form["rating1-drop"]
            if request.form["updated1"]:
                updated = request.form["updated1"]
                updatedDrop = request.form["updated1-drop"]
            else:
                updated = ""
                updatedDrop = request.form["updated1-drop"]
            if request.form["protocol1"]:
                protocol = request.form["protocol1"]
            else:
                protocol = ""
            if request.form["tag1"]:
                tag = request.form["tag1"]
            else:
                tag = ""
            if request.form["category1"]:
                category = request.form["category1"]
            else:
                category = ""
            if request.form["summary1"]:
                summary = request.form["summary1"]
            else:
                summary = ""
            if request.form["description1"]:
                description = request.form["description1"]
            else:
                description = ""

        if "submitButtonGetMashup" in request.form:
            print("In mashup: ")
            # print(request.form["title2"])
            apitype = "Mashup"

            if request.form['title2']:
                title = request.form["title2"]
            else:
                title = ""

            if request.form['rating2']:
                rating = request.form["rating2"]
                ratingDrop = request.form["rating2-drop"]
            else:
                rating = ""
                ratingDrop = request.form["rating2-drop"]
            if request.form["updated2"]:
                updated = request.form["updated2"]
                updatedDrop = request.form["updated2-drop"]
            else:
                updated = ""
                updatedDrop = request.form["updated2-drop"]
            if request.form["label2"]:
                label = request.form["label2"]
            else:
                label = ""
            if request.form["tag2"]:
                tag = request.form["tag2"]
            else:
                tag = ""
            if request.form["APIname"]:
                APIname = request.form["APIname"]
            else:
                APIname = ""
            if request.form["summary2"]:
                summary = request.form["summary2"]
            else:
                summary = ""
            if request.form["description2"]:
                description = request.form["description2"]
            else:
                description = ""

        result=mongo_query.query_results([title,rating,ratingDrop,updated,updatedDrop,protocol,tag,category,summary,description,APIname,label],apitype)
        fin_result=[]
        for i in range(len(result)):
            if fin_result:
                fin_result[0].append(result[i].split(','))
            else:
                fin_result.append(result[i].split(','))
            # print("in loop",i," ",fin_result)
        # print(result[0].split(','))
        # print(fin_result)
        return render_template('result.html', type=apitype, result=fin_result[0])




    else:
        # redirect(request.url)
        return render_template('index.html', ISO="")
    return render_template('index.html', type=apitype, result=result)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

