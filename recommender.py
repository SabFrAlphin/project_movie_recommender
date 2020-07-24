import pandas as pd
import numpy as np
import pickle
import csv

# from application import flask_user_input
from fuzzywuzzy import process

# load the movies movies_list
with open('data/movies_csv.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    movies_list = list(reader)
    movies_list = movies_list[0]


def movie_recommender(flask_user_input):
    # Load the model from a binary file
    model = pickle.load(open('data/nmf_model_binary', 'rb'))

    # Create a user input vector
    new_user_vector = pd.DataFrame([np.nan]*len(movies_list), index=movies_list).transpose()

    # Fill in the ratings
    for key, value in flask_user_input.items():
        if key in new_user_vector:
            new_user_vector.loc[:, key] = float(value)
        else:
            closest_match = process.extract(key, movies_list)[0][0]
            new_user_vector.loc[:, closest_match] = float(value)

    # Fill in the missing values
    new_user_vector_filled = new_user_vector.fillna(2.5)

    # Calculate the hidden profile with nmf.transform
    hidden_profile = model.transform(new_user_vector_filled)

    # Calculate the predictions using np.dot
    rating_predictions = pd.DataFrame(
        np.dot(hidden_profile, model.components_), columns=movies_list)

    # Find the movies that have not yet been seen
    bool_mask = np.isnan(new_user_vector.values[0])
    movies_not_seen = rating_predictions.columns[bool_mask]
    # Find recommendations for unseen movies
    movies_not_seen_df = rating_predictions[movies_not_seen].T
    # Get recommendations
    rec_list = movies_not_seen_df.sort_values(by=0, ascending=False).index[:5]
    return rec_list
