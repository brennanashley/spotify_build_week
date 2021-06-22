"""Data visualization functions"""

from fastapi import APIRouter, HTTPException
import matplotlib.pyplot as plt
import base64
import io
import pandas as pd

router = APIRouter()


@router.get('/image')
async def radar_map(song_id):
        """Route for returning radar graph."""
        df = pd.read_csv("https://raw.githubusercontent.com/brennanashley/DS-Build-3-Spotify/main/spotify_data.csv")
        c = ["acousticness", "danceability", "energy", "valence"]  # Columns to Show
        N = len(c)
        values = df[df["track_id"] == song_id].iloc[0][c].tolist()
        values += values[:1]
        print(values)
        angles = [n / float(N) * 2 * 3.141 for n in range(N)]
        angles += angles[:1]
        print(angles)
        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], c, color='grey', size=8)
        plt.yticks([], [], color="grey", size=7)
        ax.set_rlabel_position(0)
        ax.plot(angles, values, linewidth=1, linestyle='solid')
        ax.fill(angles, values, 'b', alpha=0.1)
        pic_bytes = io.BytesIO()
        plt.savefig(pic_bytes, format="png")
        pic_bytes.seek(0)
        data = base64.b64encode(pic_bytes.read()).decode("ascii")
        plt.clf()
        return "<img src='data:image/png;base64,{}'>".format(data)
