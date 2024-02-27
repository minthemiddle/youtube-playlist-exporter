#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import pandas as pd
from pytube import Playlist
from pytube.exceptions import VideoUnavailable, VideoPrivate
import time

def extract_video_info(playlist_id):
    """
    Extracts video IDs and names from a YouTube playlist.

    :param playlist_id: ID of the YouTube playlist.
    :return: DataFrame with video ID and name, and list of video IDs.
    """
    playlist = Playlist(f"https://www.youtube.com/playlist?list={playlist_id}")
    video_data = []
    for video in playlist.videos:
        video_id = video.video_id
        video_data.append({"ID": video_id, "Name": video.title})
        print(f"Processed video: {video.title}")
    return pd.DataFrame(video_data), [video["ID"] for video in video_data]


def save_to_csv(df, filename):
    """
    Saves video ID and name to a CSV file using Pandas.

    :param df: DataFrame containing video ID and name.
    :param filename: Name of the CSV file to save.
    """
    df.to_csv(f"{filename}.csv", index=False)
    print(f"CSV file saved as {filename}.csv")

def save_to_txt(video_ids, filename):
    """
    Saves video IDs to a text file.

    :param video_ids: List of video IDs.
    :param filename: Name of the text file to save.
    """
    with open(f"{filename}.txt", "w") as txtfile:
        for video_id in video_ids:
            txtfile.write(f"{video_id}\n")
    print(f"Text file saved as {filename}.txt")

@click.command()
@click.option('--playlist_id', '-pl', required=True, help='ID of the YouTube playlist')
@click.option('--name', '-n', default='playlist', help='Base name for generated files', )
@click.option('--wait', '-w', default=0, help='Wait specified seconds between processing videos', type=int)
def main(playlist_id, name, wait):
    """
    Backs up a YouTube playlist into CSV and/or txt file using Click and Pandas.
    """
    start_time = time.time()
    print("Processing playlist...")
    video_df, video_ids = extract_video_info(playlist_id)

    if wait > 0:
        print(f"Waiting {wait} seconds between requests...")
        time.sleep(wait)

    if not video_df.empty:
        save_to_csv(video_df, name)
    if video_ids:
        save_to_txt(video_ids, name)

    total_time = time.time() - start_time
    print(f"--- Total time spent: {total_time} seconds ---")

if __name__ == "__main__":
    main()
