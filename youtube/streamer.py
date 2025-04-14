# Try to stream a youtube video with innertube
from dataclasses import dataclass, field
from datetime import time

from innertube import InnerTube, config
from pytube import request

from urllib.error import HTTPError
import os

import moviepy

VIDEO_MP4 = "video/mp4"
AUDIO_MP4 = "audio/mp4"


@dataclass
class Stream:

    itag: int
    url: str
    mimeType: str
    bitrate: int
    initRange: dict
    indexRange: dict
    lastModified: int
    contentLength: int
    quality: str
    projectionType: str
    averageBitrate: float
    approxDurationMs: int

    width: int = 0
    height: int = 0
    fps: int = 0
    qualityLabel: str = ""

    audioQuality: str = ""
    audioSampleRate: int = 0
    audioChannels: int = 0
    loudnessDb: float = 0
    trackAbsoluteLoudnessLkfs: float = 0
 
    highReplication: bool = False
    codecs: str = ""

    def __post_init__(self):
        try: 
            self.codecs = self.mimeType.split(";")[1].strip().replace('"',"").split("=")[1]
            self.mimeType = self.mimeType.split(";")[0]
        
        except Exception as e:
            self.codecs = "undefined"
            self.mimeType = "undefined"
        
        try:
            self.contentLength = int(self.contentLength)
        except Exception as e:
            print(e)
    
def _get_streams_for(client_type:str, video_id: str) -> list[Stream]:
    """get all sreams for video_id and client_type"""
    streams: list[Stream] = []
    client = None
    try:
        client = InnerTube(client_type)
    except Exception as e:
        print(e)
    
    if client is not None:
        # Fetch the player data for the video
        
        data = client.player(video_id)
                
        # video details
        # data['videoDetails']
        # dict_keys(['videoId', 'title', 'lengthSeconds', 'channelId', 'isOwnerViewing', 'shortDescription', 
        # 'isCrawlable', 'thumbnail', 'allowRatings', 'viewCount', 'author', 'isPrivate', 'isUnpluggedCorpus', 
        # 'isLiveContent'])


        # List of streams of the video
        if "streamingData" in data:
            _streams = data["streamingData"].get("adaptiveFormats", [])
            print(f"There are {len(_streams)} in streamingData.adaptiveFormats")
            for _stream in _streams:
                try:
                    stream = Stream(**_stream)
                    streams.append(stream)
                except Exception as e:
                    print(e)
    return streams

def _test_urls(streams: list[Stream], allowed_mime_types: list[str]=[]) -> list[Stream]:
    """return allowed streams"""
    print("allowed_mime_types:", allowed_mime_types)
    allowed_streams = []
    for stream in streams:
        allowed = False
        if len(allowed_mime_types) > 0:
            if stream.mimeType in allowed_mime_types:
                allowed = True
        else:
            allowed = True
        if allowed:
            try:
                result = request.head(url=stream.url)
                content_length = int(result['content-length'])
                if stream.contentLength != content_length:
                    print(f"There is a missmatch in content length: {stream.contentLength} vs {content_length}")
                else:
                    allowed_streams.append(stream)
            except Exception as e:
                print(e)
    print(f"{len(allowed_streams)} Streams selected")
    return allowed_streams

def _download(url: str, content_length: int, file_path: str, timeout=None, max_retries=0):
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
                print("bytes remaining",bytes_remaining)
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

def download(path, video_id: str, 
             client: str, 
             allowed_mime_types: list=[VIDEO_MP4, AUDIO_MP4],
             q=True) -> list[str, Stream]:
    
    n_downloaded = 0
    files = []
    streams = _get_streams_for(client_type=client, video_id=video_id)
    allowed_streams = _test_urls(streams, allowed_mime_types=allowed_mime_types)

    video_allowed_streams = [(stream.width*stream.height ,stream) for stream in allowed_streams if stream.mimeType == VIDEO_MP4]
    audio_allowed_streams = [(stream.width*stream.height ,stream) for stream in allowed_streams if stream.mimeType == AUDIO_MP4]
    
    video_allowed_streams = sorted(video_allowed_streams, key=lambda x:x[0], reverse=True)
    audio_allowed_streams = sorted(audio_allowed_streams, key=lambda x:x[0], reverse=True)
    if q:
        allowed_streams = []
        if len(video_allowed_streams) > 0:
            allowed_streams.append(video_allowed_streams[0])
        if len(audio_allowed_streams) > 0:
            allowed_streams.append(audio_allowed_streams[0])

    for (q, stream) in allowed_streams:
        print(stream.contentLength)
        if not os.path.exists(path):
            os.mkdir(path)

        file_path = f"{path}{os.sep}{video_id}_{client}_{stream.itag}_{stream.codecs}_{stream.quality}.mp4"
        _download(url=stream.url, 
                  content_length=stream.contentLength, 
                  file_path=file_path)
        files.append((file_path, stream))
        n_downloaded += 1

    return files


def combine_video_with_audio(video_filepath: str,
                             audio_filepath: str,
                             output_file: str):
    
    video_clip = moviepy.VideoFileClip(video_filepath)
    audio_clip = moviepy.AudioFileClip(audio_filepath)

    video_clip_with_audio = video_clip.with_audio(audio_clip)
    video_clip_with_audio.write_videofile(output_file, audio_codec="aac")

    

if __name__ == "__main__":
    path = "./data/tmp"
    video_id = "BHBAnUAdeyE"
    #video_id = "_p0S_zZd4NQ"
    client = "IOS"
    video_files = download(path=path, video_id=video_id, client=client, allowed_mime_types=[VIDEO_MP4])
    print(f"{len(video_files)} video files downloaded.")
    audio_files = download(path=path, video_id=video_id, client=client, allowed_mime_types=[AUDIO_MP4])
    print(f"{len(audio_files)} audio files downloaded.")
    
    # now combine audio and video
    video_filepath, video_stream = video_files[0]
    audio_filepath, audio_stream = audio_files[0]

    output_file = f"./data/{video_id}.mp4"
    combine_video_with_audio(video_filepath=video_filepath,
                             audio_filepath=audio_filepath,
                             output_file=output_file)




