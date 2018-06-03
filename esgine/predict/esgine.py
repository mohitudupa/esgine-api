import random
import datetime
import pandas as pd


topics = ["science", "politics", "literature", "art", "news", "music", "movies", "health"]


class Esgine():
    def predict(self, file_name):
        df = pd.read_csv(file_name)
        result = {}

        for i in range(len(df)):
            topic = random.choice(topics)
            confidence = random.randrange(0, 1000) / 1000

            result[i] = {
                        "para": df.loc[i][0],
                        "topic": topic,
                        "confidence": confidence,
            }

        return result
