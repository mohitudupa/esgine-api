from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render, redirect
import re
# from sklearn import *
import numpy as np
import os
from io import StringIO
import pandas as pd


# import required packages


# Remove this package after integration
import random
from .esgine import Esgine


# Regular expression to validate text encoding
text_re = r'^((.)+(\n)*)+$'


# Creating an object of the Esgine class
esgine = Esgine();


# Generaring a unique temp file name
def get_file_name():
    while 1:
        file = "temp" + str(random.random())[2:]
        if os.path.isfile(file):
            continue
        return(file)



def predict(request):
    if request.method == 'GET':
        x = dict(request.POST)

        return render(request, 'predict/home.html', {"result": False, "error": False})

    if request.method == 'POST':
        data = dict(request.POST)
        error = {"error": []}
        text = b""

        try:
            # Validating the type of input data
            file = request.FILES["file"]

            if str(type(file)) != "<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>":
                error["error"].append("Invalid value-type for key: file")

            # Reading the text file
            for chunk in file.chunks():
                text += chunk
            text = text.decode()

            # Validating the format of the contents of the text file
            if not bool(re.match(text_re, text)):
                print()
                error["error"].append("Invalid contents of text file")

            # Validating (parsing) the csv file
            pd.read_csv(StringIO(text))


        except UnicodeDecodeError:
            error["error"].append("Invalid text encoding")
        except (KeyError, AttributeError):
            error["error"].append("A csv file must be uploaded")
        except pd.errors.ParserError:
            error["error"].append("Invalid csv file")

        if error["error"]:
            return render(request, 'predict/home.html', {"result": False, "errors": error["error"]})

        # Saving as a temp file
        file_name = get_file_name()

        # Writing contents into temp file
        f = open(file_name, "w")
        f.write(text)
        f.close()

        # Calling the predict function
        result = esgine.predict(file_name)

        # Removing the temp file
        os.remove(file_name)

        # Reformatting results for jinja template
        final = [result[i] for i in result] 
    
        return render(request, 'predict/home.html', {"result": True, "error": False, "paras": final})