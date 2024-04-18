from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, vfx, VideoFileClip
import pyttsx3 
import os
import requests
import shutil

def make_audios_clone_voice(script="script"):
    with open(f"Long form Videos/{script}.txt") as t:
                lines = t.readlines()
    text = ''
    texts = []
    voice = pyttsx3.init()
    for e in lines:
        if e == '\n':
            texts += [text]
            text = ''
        else:
            text += e
    for text in texts:

        response = requests.post("http://127.0.0.1:7860/run/generate", json={
            "data": [
                text,
                "hello world",
                "None",
                "hello world",
                "me",
                {"name":"audio.wav","data":"data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="},
                0,
                1,
                0,
                16,
                30,
                0.2,
                "P",
                8,
                0,
                0.8,
                1,
                1,
                2,
                2,
                ["Half Precision"],
                False,
                False,
            ]
        }).json()

        data = response["data"]
        shutil.copy2(data[0]['name'],f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos\Audios/audio{texts.index(text)+1}.wav")

def create_audio(script="script"):
    with open(f"Long form Videos/{script}.txt") as t:
            lines = t.readlines()
    text = ''
    texts = []
    voice = pyttsx3.init()
    for e in lines:
        if e == '\n':
            texts += [text]
            text = ''
        else:
            text += e
    index = 0
    for text in texts:
        index += 1
        if text != '.\n':
            voice.save_to_file(text,f"Long form Videos/audios/audio{index}.mp3")
            voice.runAndWait()
def create_video(frame_num,video_name="video1", audio_file_ext=".mp3",audio_index=1,delay=0.5,external_audio=False):
    clips = []
    index = audio_index
    while index < frame_num + 1 + audio_index:
        if index == frame_num + audio_index:
            image1 = ImageClip("Long form Videos/resources/background.png")
            Video1 = image1.set_duration(5)
        else:
            audio1 = AudioFileClip(f'Long form Videos/audios/audio{index}{audio_file_ext}')
            image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
            clip1 = image1.set_duration(audio1.duration+delay)
            Video1= clip1.set_audio(audio1)
        if external_audio:
            try:
                audio1 = AudioFileClip(f'Long form Videos/audios/audio{index}{audio_file_ext}')
                image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
                clip1 = image1.set_duration(audio1.duration+delay)
                Video1= clip1.set_audio(audio1)
            except:
                if index == 56: # No goal
                    audio1 = AudioFileClip(f'Long form Videos/no-goal.mp3')
                    image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(audio1.duration)
                    Video1 = clip1.set_audio(audio1)
                elif index == 69:
                    image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(3)
                    Video1 = clip1
                elif index == 49:
                    image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(0.5)
                    Video1 = clip1
                else:
                    audio1 = AudioFileClip(f'Long form Videos/goal{audio_file_ext}')
                    image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(audio1.duration)
                    Video1 = clip1.set_audio(audio1)
        clips += [Video1]
        index += 1
    
    Video_final = concatenate_videoclips(clips)
    Video_final.write_videofile(f'Long form Videos/{video_name}.mp4',24)
def apendimage2video(path_video='Long form Videos/video1.mp4',path_image='Long form Videos/Frames/69.png',output='Long form Videos/video.mp4',img_duration=3):
    video1 = VideoFileClip(path_video)
    video2 = ImageClip(path_image).set_duration(img_duration)
    Video_final = concatenate_videoclips([video1,video2])
    Video_final.write_videofile(output,24)
    

create_video(46)