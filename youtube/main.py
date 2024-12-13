###############################################################################
#
# Quick Fix for downloading Youtube videos until PyTube 15.0.0 will be repaired
#
###############################################################################

import os
import sys
import json
from typing import Union, List
import argparse
import logging
import requests
from urllib.parse import urlparse

from pytube import Playlist, YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from re_punctuation import PunctuationModel

# Deep Learning Lecture of Andreas Geiger from University of Tübnigen 
#URL = "https://www.youtube.com/playlist?list=PL05umP7R6ij3NTWIdtMbfvX7Z-4WEXRqD"
#URL = "https://www.youtube.com/watch?v=vRTcE19M-KE"

def _check_url(url:str) -> tuple[str, str]:
    """checks youtube url and return playlist or video id"""
    video_id, playlist_id = None, None
    print(f"url: {url}")
    u = urlparse(url=url)
    if u.netloc != "www.youtube.com":
        print(f"url mus contain correct net location not {u.netloc}")
        return None, None
    
    query = u.query.split("=")
    if len(query) < 2:
        print(f"url must contain a avild query (query={query}).")
        return None, None
    
    if u.path == "/watch":
        if query[0] != "v":
            print(f"for playlist extraction url must contain a avild query (query={query}).")
            return None, None        
        video_id = query[1]

    elif u.path == "/playlist":
        if query[0] != "list":
            print(f"for playlist extraction url must contain a avild query (query={query}).")
            return None, None 
        playlist_id = query[1]

    else:
        print(f"url must contain /watch or /playlist in path, not {u.path}.")
        return None, None

    try:
        page = requests.head(url)
        print(f"url is reachable: {page.status_code}")
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(f"url is not reachable: {e}")
        return None, None

    return playlist_id, video_id

def _find(html: str, tag: str):
    result = '"'
    start = html.find(tag)
    j = start + len(tag)
    while True:
        letter = html[j]
        result += letter
        j += 1
        if letter == '\\':
            result += html[j]
            j += 1
        elif letter == '"':
            break
    return start, result

def _load_playlist(url:str) -> Union[Playlist, dict]:
    playlist = Playlist(url)
    print("title      :",playlist.title)
    metadata = playlist.initial_data.get("metadata", {})
    playlistMetadataRenderer = metadata.get("playlistMetadataRenderer", {})
    description = playlistMetadataRenderer.get("description", "")
    print("description:",description)
    print("id         :",playlist.playlist_id)
    print("url        :",playlist.playlist_url)
    print("owner      :",playlist.owner)
    print("owner id   :",playlist.owner_id)
    print("owner url  :",playlist.owner_url)
    print("updated    :",playlist.last_updated)
    print("length     :",playlist.length)

    playlist_dict = {}
    playlist_dict["id"] = playlist.playlist_id
    playlist_dict["url"] = playlist.playlist_id
    playlist_dict["title"] = playlist.title
    playlist_dict["description"] = description
    playlist_dict["owner"] = playlist.owner
    playlist_dict["owner_id"] = playlist.owner_id
    playlist_dict["owner_url"] = playlist.owner_url
    playlist_dict["updated"] = str(playlist.last_updated)
    playlist_dict["videos"] = []
    
    return playlist, playlist_dict

def _load_video(video) -> dict:
    
    print("video url  :", video.watch_url)

    html = video.watch_html
    j, title = _find(html=html, tag='"title":"')
    print(f"video tag at {j}:", title)
    j, description = _find(html=html, tag='"shortDescription":"')
    print(f"video description at {j}:", description) 
    #j, details = _find(html=html, tag='"videoDetails":"')
    #print(f"video details at {j}:", details)    
    print(80*"=")
    
    video = {
        "id": video.video_id,
        "url": video.watch_url,
        "title": title,
        "description": description,
        "author": video.author,
        "publish_dat": str(video.publish_date),
        "rating": video.rating,
    }
    return video

def _load_video_transcript(video_id: str) -> dict:
    # Retrieve the transcript
    print(f"retrieve transcript for {video_id}")
    transcript = {}
    try:    
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Transcript has {len(transcript)} chunks.")
    except Exception as e:
        print(e)
        return {}
    return transcript

def _preprocess_transcript(transcript_dict: dict, model: PunctuationModel) -> List[str]:        
    
    if transcript_dict == {} or len(transcript_dict) == 0:
        return []
    text = [chunk['text'] for chunk in transcript_dict]         
    text = " ".join(text)
    print(f"all chunks aggregated: {len(text)} characters")
    words = text.split(" ")
    print(f"all chunks aggregated: {len(words)} words")        
    
    # re-punctuation
    result = model.restore_punctuation(text)
    """
        stepsize = 500 # depends on context window size of 1024
        results = []
        for i in range(0, len(words), stepsize):
            if (i + stepsize) < len(words):
                input_text = " ".join(words[i:stepsize])
            else:
                input_text = " ".join(words[i:-1])
            
            print("input text", len(input_text))
            result = model.restore_punctuation(input_text)
            results.append(result)

        result = " ".join(results)    
    
    """
    #sentence splitting
    
    sentences =  sent_tokenize(text=result) #, language=language)
    return sentences

if __name__ == "__main__":

    #######
    parser = argparse.ArgumentParser(description="Download Youtube files and extract data")
    parser.add_argument("--url", help="Playlist or Video URL", type=str, required=True)
    parser.add_argument("--out", help="Output path: where to store the extracted videos", 
                        type=str, default=f".{os.sep}data")
    args = parser.parse_args()

    playlist_id, video_id = _check_url(url=args.url)
    if playlist_id is None and video_id is None:
        print("No valid url. Program aborded!")
        sys.exit()
    else:
        print("playlist_id:", playlist_id)
        print("video_id   :", video_id)

    print("load models for re-punctuation and grammar correction")

    # https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large
    from re_punctuation import PunctuationModel as PunctuationModel
    model = PunctuationModel(model="oliverguhr/fullstop-punctuation-multilang-large")

    # https://huggingface.co/vennify/t5-base-grammar-correction
    from happytransformer import HappyTextToText, TTSettings
    happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
    tt_settings = TTSettings(num_beams=5, min_length=1, max_length=300)

    print("all models loaded")

    # setup directories
    output_path = args.out
    if not os.path.exists(path=output_path):
        os.mkdir(output_path)
        print(f"directory {output_path} created")

    videos = []
    if playlist_id is not None:
        playlist, playlist_dict = _load_playlist(args.url)
        if playlist_id != playlist_dict['id']:
            print("Warning: loaded playlist not identical to playlist id in url!")

        output_path = f"{output_path}{os.sep}{playlist_dict['id']}"
        if not os.path.exists(path=output_path):
            os.mkdir(output_path)
            print(f"directory {output_path} created")

        print(f"Extract videos from playlist: {playlist_dict['id']}")
        videos: list[YouTube] = list(playlist.videos)

    elif video_id is not None:
        video = YouTube(url=args.url) 
        videos: list[YouTube] = [video]

    else:
        #should not happen
        import pdb; pdb.set_trace()
        sys.exit()

    #extract videos
    for i, video in enumerate(videos):
        
        print("video id   :", video.video_id)
        video_dict = _load_video(video)
        if playlist_id is not None:
            playlist_dict['videos'].append(video_dict)
        
        video_id = video_dict['id']

        video_path = f"{output_path}{os.sep}{video_id}"
        if os.path.exists(path=video_path):
            print(f"video {video_id } already downloaded. Skipped!")

        else:
            os.mkdir(video_path)
                    
            stream = video.streams.get_highest_resolution()
            video_dict["resolution"] = stream.resolution
            video_dict["filesize"] = stream.filesize
            video_dict["codecs"] = stream.codecs

            with open(f"{video_path}{os.sep}video.json", "w") as f:
                f.write(json.dumps(video_dict, indent=3))

            stream.download(output_path=video_path, filename=f"{video_id}.mp4")

            transcript_dict = _load_video_transcript(video_id=video_id)
            with open(f"{video_path}{os.sep}transcription.json", "w") as f:
                f.write(json.dumps(transcript_dict, indent=3))

            ############# now all vido data are loaded and saved to disc ############
            #
            # start data pre processing 
            #
            #########################################################################
            
            sentences = _preprocess_transcript(transcript_dict=transcript_dict, model=model)
            print(f"sentences extracted {len(sentences)}")
            with open(f"{video_path}{os.sep}sentences.txt", "w") as f:
                f.write("\n".join(sentences))

            # run grammar correction
            grammar_corrected = []
            for i, sentence in enumerate(sentences):
                # Add the prefix "grammar: " before each input 
                result = happy_tt.generate_text(f"grammar: {sentence}", args=tt_settings)
                print(i, result.text) 
                grammar_corrected.append(result.text)

            with open(f"{video_path}{os.sep}grammar_corrected_sentences.txt", "w") as f:
                f.write("\n".join(grammar_corrected))

    if playlist_id is not None:
        with open(f"{output_path}{os.sep}playlist.json", "w") as f:
            f.write(json.dumps(playlist_dict, indent=3))   
    
    print("finished")