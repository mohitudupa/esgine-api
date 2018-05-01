from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import re
import datetime
from sklearn import *
import numpy as np


# import required packages


# Remove this package after integration
import random


text = r'^((.)+(\n)*)+$'


# Remove this function after integrating the predict call of the model
def predict(para):
    topics = ["science", "politics", "literature", "art", "news", "music", "movies", "health"]
    topic = random.choice(topics)
    confidence = random.randrange(0, 1000) / 1000
    return([topic, confidence])


def run_cases(paras):
    res = {}
    for i in range(len(paras)):
        # Call the predict function on the required model for every paragraph.
        # res.append(model.predict(paras[i]))

        # Asuming that the predict function will return a list(or a numpy array) with the topic as the 0th element and confidence as the 1st element
        # This is a dummy predict function implementation
        prediction = predict(paras[i])
        result = prediction

        res[i] = {
            "para": paras[i],
            "topic": result[0],
            "confidence": result[1]
        }

    return res


class Predict(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        error = {"error": []}
        text_data = b""
        paras = []

        try:
            # Validating the type of input data
            if str(type(data["text"])) != "<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>":
                error["error"].append("Invalid value-type for key: text")

            # Reading the text file
            for chunk in request.data['text'].chunks():
                text_data += chunk
            text_data = text_data.decode()

            # Validating the format of the contents of the text file
            if not bool(re.match(text, text_data)):
                error["error"].append("invalid contents of text file")

        except KeyError:
            error["error"].append("The following key is required: text")
        except AttributeError:
            error["error"].append("A text file must be uploaded")

        if error["error"]:
            return Response(error)

        # Splitting the data
        # Asuming that every paragraph is sapeerated by 2 new-line characters
        for i in text_data.split("\n\n"):
            if i != "":
                paras.append(i.strip())

        # Running predictions on the model
        result = run_cases(paras)

        # Returning result dictionary
        return Response(result)