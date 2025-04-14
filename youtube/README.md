# Data Extraction

##  Youtube Data Extraction

### Understand Youtube URLs

<https://www.youtube.com/watch?v=BHBAnUAdeyE>
<https://www.youtube.com/watch?v=UNbLjVEYvLQ>

The same video as part of a playlist
<https://www.youtube.com/watch?v=BHBAnUAdeyE&list=PL05umP7R6ij3NTWIdtMbfvX7Z-4WEXRqD&index=1>

How to extract all titles of a playlist?
<https://www.youtube.com/playlist?list=PL05umP7R6ij3NTWIdtMbfvX7Z-4WEXRqD>

### How to extract YouTube data

1. Extract Youtube Website with BeautifulSoup
2. Download video with pytube and innertube
    -<https://pypi.org/project/pytube2/>
    - <https://pytube.io/en/latest/>
3. Use the Youtube API
4. Download vido transcription with youtube-transcript-api
    - <https://pypi.org/project/youtube-transcript-api/>
    - <https://medium.com/chat-gpt-now-writes-all-my-articles/extract-youtube-video-transcripts-for-free-in-python-then-summarize-the-videos-with-openai-2234d944232a>

```bash
conda create --name "youtube" -python=3.12
conda activate youtube
pip install pytube2 
pip install innertube
pip install youtube-transcript-api
pip install moviepy
```

## Use moviepy to combine or extract audio from video.

```code
def combine_audio(vidname, audname, outname, fps=25):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)
```


## Grammer Correction and Re-Punctuation

```bash
pip install transformers
pip install sentencepiece
pip install happytransformer
pip install nltk

python
>>> import nltk
>>> nltk.download('punkt_tab')
```

## Scene Detection

```bash
pip install scenedetect
pip install opencv-python
```


## Download and Extract

```bash
python main.py --url <playlist or video url> --out <path to output>

```
