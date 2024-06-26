from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
from ScriptWriter import translate
import pyttsx3 
import os
import sys
import requests
import shutil
# This makes the code think is in the root folder. Only done for organizing
sys.path.append("C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code")

def create_vid(images,script='script',output="video1",clone=False,make_audio=True):
    videoclips = []
    for img in images:
        if make_audio:
            if not clone:
                with open(f"{script}.txt") as t:
                    lines = t.readlines()
                text = ''
                texts = []
                voice = pyttsx3.init()
                voice.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
                for e in lines:
                    if e == '\n':
                        texts += [text]
                        text = ''
                    else:
                        text += e
                index = 0
                for text in texts:
                    index += 1
                    voice.save_to_file(text,f"audio{index}.mp3")
                    voice.runAndWait()


        if not clone:
            audio = AudioFileClip(f'audio{images.index(img)+1}.mp3')
        else:
            audio = AudioFileClip(f'audio{images.index(img)+1}.wav')

        image = ImageClip(f'Video Output/{img}.png')
        clip = image.set_duration(audio.duration)
        Video= clip.set_audio(audio)
        videoclips += [Video]
    Video_final = concatenate_videoclips(videoclips)
    Video_final.write_videofile(f'Youtube Output/{output}.mp4',24)
    for img in images:
        if not clone:
            os.remove(f'audio{images.index(img)+1}.mp3')
        else:
            os.remove(f'audio{images.index(img)+1}.wav')
            
def create_short(img1="Video",img2="Video-1",img3="Video-2",script='sort_script',clone=False,make_audio=True):
    if make_audio:
        if not clone:
            with open(f"{script}.txt") as t:
                lines = t.readlines()
            text = ''
            texts = []
            voice = pyttsx3.init()
            voice.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
            for e in lines:
                if e == '\n':
                    texts += [text]
                    text = ''
                else:
                    text += e
            voice.save_to_file(texts[0],"audio1.mp3")
            voice.save_to_file(texts[1],"audio2.mp3")
            voice.runAndWait()
        else:
            make_audios_clone_voice(script)
    if not clone:
        audio1 = AudioFileClip('audio1.mp3')
        audio2 = AudioFileClip('audio2.mp3')
    else:
        audio1 = AudioFileClip('audio1.wav')
        audio2 = AudioFileClip('audio2.wav')

    image1 = ImageClip(f'Video Output/{img1}.png')
    image2 = ImageClip(f'Video Output/{img2}.png')
    image3 = ImageClip(f'Video Output/{img3}.png')
    
    clip1 = image1.set_duration(audio1.duration/2)
    clip2 = image2.set_duration(audio1.duration/2)
    clip1 = concatenate_videoclips([clip1,clip2])
    
    clip2 = image3.set_duration(audio2.duration)
    
    Video1= clip1.set_audio(audio1)
    Video2= clip2.set_audio(audio2)
    Video_final = concatenate_videoclips([Video1,Video2])
    Video_final.write_videofile('Youtube Output/short.mp4',24)
    if not clone:
        os.remove('audio1.mp3')
        os.remove('audio2.mp3')
    else:
        os.remove('audio1.wav')
        os.remove('audio2.wav')

def make_translation(script="script",sort="sort_script"):
    script = translate(script)
    sort = translate(sort)
    make_audio(script,'script_es')
    make_audio(sort,'sort_es')

def make_audio(texts,output="es_audio"):
    voice =pyttsx3.init()
    voice.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0')
    audios = []
    for text in texts:
        voice.save_to_file(text,f"audio.mp3")
        voice.runAndWait()
        audios += [AudioFileClip('audio.mp3')]
    audios = concatenate_audioclips(audios)
    audios.write_audiofile(f"Youtube Output/{output}.mp3")
    os.remove('audio.mp3')
    
def make_audios_clone_voice(script="script"):
    with open(f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code\{script}.txt") as t:
        lines = t.readlines()
    text = ''
    texts = []
    for e in lines:
        if e == '\n':
            texts += [text]
            text = ''
        else:
            text += e
    for text in texts:
        if text != '':
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
                    5,
                    4,
                    ["Half Precision"],
                    False,
                    False,
                ]
            }).json()
            print(f"audio({texts.index(text)+1}) done")
            data = response["data"]
            shutil.copy2(data[0]['name'],f"C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code/audio{texts.index(text)+1}.wav")

