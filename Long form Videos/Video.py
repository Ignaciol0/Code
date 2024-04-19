from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, vfx, VideoFileClip, concatenate_audioclips
import pyttsx3 
import os
import requests
import sys
sys.path.append("C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code")

from ScriptWriter import translate
import shutil

def make_audios_clone_voice(script="script"):

    with open(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/{script}.txt") as t:
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

def create_audio(script="script",language="en",multiple=True):
    with open(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/{script}.txt") as t:
            lines = t.readlines()
    texts = lines
    voice = pyttsx3.init()
    if language == 'en':
        voice.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
    elif language == 'es':
        voice.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0')
    index = 0
    audios = []
    if multiple:
        for text in texts:
            index += 1
            if text != '\n':
                voice.save_to_file(text,f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audios/audio{index}.mp3")
                voice.runAndWait()
    else:
        for text in texts:
            if text != '\n':
                voice.save_to_file(text,f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audio.mp3")
                voice.runAndWait()
                audios += [AudioFileClip(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audio.mp3")]
        audios = concatenate_audioclips(audios)
        audios.write_audiofile(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/{language}_audio.mp3")
        os.remove(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audio.mp3")
def create_video(frame_num,video_name="video1", audio_file_ext=".mp3",audio_index=1,delay=0.5,external_audio=False):
    clips = []
    index = audio_index
    while index < frame_num + 1 + audio_index:
        if index == frame_num + audio_index:
            image1 = ImageClip("C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/resources/background.png")
            Video1 = image1.set_duration(5)
        else:
            audio1 = AudioFileClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audios/audio{index}{audio_file_ext}')
            image1 = ImageClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/Frames/{index}.png')
            clip1 = image1.set_duration(audio1.duration+delay)
            Video1= clip1.set_audio(audio1)
        if external_audio:
            try:
                audio1 = AudioFileClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audios/audio{index}{audio_file_ext}')
                image1 = ImageClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/Frames/{index}.png')
                clip1 = image1.set_duration(audio1.duration+delay)
                Video1= clip1.set_audio(audio1)
            except:
                if index == 56: # No goal
                    audio1 = AudioFileClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/no-goal.mp3')
                    image1 = ImageClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(audio1.duration)
                    Video1 = clip1.set_audio(audio1)
                elif index == 69:
                    image1 = ImageClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(3)
                    Video1 = clip1
                elif index == 49:
                    image1 = ImageClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(0.5)
                    Video1 = clip1
                else:
                    audio1 = AudioFileClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/goal{audio_file_ext}')
                    image1 = ImageClip(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/Frames/{index}.png')
                    clip1 = image1.set_duration(audio1.duration)
                    Video1 = clip1.set_audio(audio1)
        clips += [Video1]
        index += 1
    
    Video_final = concatenate_videoclips(clips)
    Video_final.write_videofile(f'C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/{video_name}.mp4',24)
def apendimage2video(path_video='Long form Videos/video1.mp4',path_image='Long form Videos/Frames/69.png',output='Long form Videos/video.mp4',img_duration=3):
    video1 = VideoFileClip(path_video)
    video2 = ImageClip(path_image).set_duration(img_duration)
    Video_final = concatenate_videoclips([video1,video2])
    Video_final.write_videofile(output,24)
def translate_video_audio(script="script", audio_output="audio.mp3", language="es"):   
    translated = translate(f"Long form Videos/{script}")
    checked_lines=[]
    for line in translated:
        if input(f"{line}\nIs it ok: ") == 'no':
            checked_lines += [input("\nHow should it be: ")]
        else:
            checked_lines += [line]
    audios = []
    for text in texts:
            voice.save_to_file(text,f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audios/{language}_audio.mp3")
            voice.runAndWait()
            audios += [AudioFileClip(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audios/{language}_audio.mp3")]
    os.remove(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audios/{language}_audio.mp3")
    audios = concatenate_audioclips(audios)
    audios.write_audiofile(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\Long form Videos/audios/{language}_{audio_output}")

create_audio("spanish_translation","es",False)