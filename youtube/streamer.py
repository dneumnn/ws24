# Try to stream a youtube video with innertube
from innertube import InnerTube, config
from typing import List
from pytube import request
from pytube.innertube import _default_clients

from urllib.error import HTTPError
import os

def _get_streams_for(client_type:str, video_id: str) -> List[dict]:
    streams = []
    client = None
    try:
        client = InnerTube(client_type)
    except Exception as e:
        print(e)
    
    if client is not None:
        # Fetch the player data for the video
        try:
            data = client.player(video_id)
            # List of streams of the video
            if "streamingData" in data:
                streams = data["streamingData"]["adaptiveFormats"]
        except Exception as e:
            print(e)

    return streams

def _get_allowed_urls(streams) -> list:
    """return allowed urls as tuple (itag, mime_type,quality, url) """
    allowed_urls = []
    for stream in streams:
        itag = stream['itag']
        url = stream['url']
        mime_type = stream['mimeType']
        quality = stream['quality']
        try:
            result = request.head(url=url)
            allowed_urls.append((itag, mime_type, quality, url))
        except Exception as e:
            print(e)
    return allowed_urls

def _download(url, content_length, file_path, timeout=None, max_retries=0):
    """forked method download from PyTube.Stream"""
    bytes_remaining = content_length
    with open(file_path, "wb") as fh:
        try:
            for chunk in request.stream(
                url,
                timeout=timeout,
                max_retries=max_retries
            ):
                # reduce the (bytes) remainder by the length of the chunk.
                bytes_remaining -= len(chunk)
                # send to the on_progress callback.
                #self.on_progress(chunk, fh, bytes_remaining)
                #print("bytes remaining",bytes_remaining)
                fh.write(chunk)
        except HTTPError as e:
            print("HTTPError: ", e)
            if e.code != 404:
                raise
            # Some adaptive streams need to be requested with sequence numbers
            for chunk in request.seq_stream(
                url,
                timeout=timeout,
                max_retries=max_retries
            ):
                # reduce the (bytes) remainder by the length of the chunk.
                bytes_remaining -= len(chunk)
                # send to the on_progress callback.
                #print("bytes remaining",bytes_remaining)
                fh.write(chunk)

def download(path, video_id: str, client: str) -> int:
    n_downloaded = 0
    streams = _get_streams_for(client_type=client, video_id=video_id)
    allowed_urls = _get_allowed_urls(streams)
    #print(allowed_urls)
    for (itag, mime_type, quality, url) in allowed_urls:
        print(mime_type)
        mime_type_item = mime_type.split(";")[0]
        codecs = mime_type.split(";")[1].strip().replace('"',"").split("=")[1]
        if mime_type_item in ["video/mp4", "audio/mp4"]:
            result = request.head(url=url)
            content_length = int(result['content-length'])
            file_path = f"{path}{os.sep}{video_id}_{client}_{itag}_{codecs}_{quality}.mp4"
            _download(url=url, content_length=content_length, file_path=file_path)
            n_downloaded += 1
    return n_downloaded

if __name__ == "__main__":
    path = "."
    video_id = "BHBAnUAdeyE"
    client = "IOS"
    download(path=path, video_id=video_id, client=client)


