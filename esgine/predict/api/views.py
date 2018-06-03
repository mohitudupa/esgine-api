from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import re
# from sklearn import *
import numpy as np
import os
import pandas as pd
from io import StringIO


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


class Predict(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        error = {"error": []}
        text = b""

        try:
            # Validating the type of input data
            if str(type(data["text"])) != "<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>":
                error["error"].append("Invalid value-type for key: text")

            # Reading the text file
            for chunk in request.data['text'].chunks():
                text += chunk
            text = text.decode()

            # Validating the format of the contents of the text file
            if not bool(re.match(text_re, text)):
                error["error"].append("Invalid contents of text file")

            # Validating (parsing) the csv file
            pd.read_csv(StringIO(text))

        except UnicodeDecodeError:
            error["error"].append("Invalid text encoding")
        except KeyError:
            error["error"].append("The following key is required: text")
        except AttributeError:
            error["error"].append("A text file must be uploaded")
        except pd.errors.ParserError:
            error["error"].append("Invalid csv file")

        if error["error"]:
            return Response(error)

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

        # Returning result dictionary
        return Response(result)