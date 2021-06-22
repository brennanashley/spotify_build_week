import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import json


def song_choice(song_id):
    df = pd.read_csv("https://raw.githubusercontent.com/brennanashley/DS-Build-3-Spotify/main/spotify_data.csv")
    # columns to drop for fitting
    c = ["duration_ms", "index", "genre", "artist_name", "track_id", "track_name", "key", "mode"]
    # get song from user input
    song = df[df["track_id"] == song_id].iloc[0]
    df_selected = df.copy()
    if not pd.isnull(song["genre"]): # If genre, set subset to only genre
        df_selected = df[df["genre"] == song["genre"]]
    # nearest neighbors
    nn = NearestNeighbors(n_neighbors=11, algorithm="kd_tree")
    nn.fit(df_selected.drop(columns=c))
    song = song.drop(index=c)
    song = np.array(song).reshape(1, -1)
    result = df_selected.iloc[nn.kneighbors(song)[1][0][1:11]].to_json(orient="records")# Return results as json
    parsed = json.loads(result)
    return json.dumps(parsed, indent=2)


print(song_choice('7FFfYM4JE1vj5n4rhHxg8q'))