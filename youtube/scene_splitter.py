# see: https://github.com/snap-research/Panda-70M/tree/main/splitting
from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg

if __name__ == "__main__":
    filename = "./data/vRTcE19M-KE.mp4"
    scene_list = detect(filename, AdaptiveDetector())
    split_video_ffmpeg(input_video_path=filename,
                       scene_list=scene_list,
                       output_dir="./data")
    print(scene_list)