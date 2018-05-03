from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import re
from sklearn import *
import numpy as np
import pickle
import pandas as pd


# import required packages


# Remove this package after integration
import random
import datetime


text = r'^((.)+(\n)*)+$'

# Loading the model object from a pickle file
# Dump the pickle data of the model into the file "model.pickle" in the root folder of the project "esgine/"
# Currently model.pickle if filled with dummy pickle data of a datetime.datetime object
# If this line thrown an error replace the filename with the absolutepath of the path
model = pickle.load(open("model.pickle", "rb"))


# Remove this function after integrating the predict call of the model
def predict(para):
    topics = ["science", "politics", "literature", "art", "news", "music", "movies", "health"]
    topic = random.choice(topics)
    confidence = random.randrange(0, 1000) / 1000
    return([topic, confidence])


def run_cases(paras):

    # Initializing the result dataframe
    df = pd.DataFrame(columns=["para", "topic", "confidence"])

    for i in range(len(paras)):
        # Call the predict function on the required model for every paragraph.
        # prediction = model.predict(paras[i])

        # Asuming that the predict function will return a list(or a numpy array) with the topic as the 0th element and confidence as the 1st element
        # This is a dummy predict function implementation
        prediction = predict(paras[i])

        # Saving the result into the dataframe
        df.loc[i] = [paras[i], prediction[0], prediction[1]]

    return df


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
                error["error"].append("Invalid contents of text file")

        except UnicodeDecodeError:
            error["error"].append("Invalid text encoding")
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
        data_frame = run_cases(paras)

        result = {}

        for i in range(len(data_frame["para"])):
            result[i] = {
                    "para": data_frame["para"][i],
                    "topic": data_frame["topic"][i],
                    "confidence": data_frame["confidence"][i],
            }

        print(data_frame)

        # Returning result dictionary
        return Response(result)