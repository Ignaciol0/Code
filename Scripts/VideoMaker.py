from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
from ScriptWriter import translate
import pyttsx3 
import os
import sys
# This makes the code think is in the root folder. Only done for organizing
sys.path.append("C:\\Users\ignac\Documents\Documentos\Football\Futty Data\Automation Code\Template\Code")

def create_vid(img1,img2,img3,script='script',output="video1"):
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
    voice.save_to_file(texts[2],"audio3.mp3")
    voice.runAndWait()


    audio1 = AudioFileClip('audio1.mp3')
    audio2 = AudioFileClip('audio2.mp3')
    audio3 = AudioFileClip('audio3.mp3')

    image1 = ImageClip(f'Video Output/{img1}.png')
    image2 = ImageClip(f'Video Output/{img2}.png')
    image3 = ImageClip(f'Video Output/{img3}.png')
    clip3 = image3.set_duration(audio3.duration)
    clip2 = image2.set_duration(audio2.duration+1)
    clip1 = image1.set_duration(audio1.duration+1)
    Video1= clip1.set_audio(audio1)
    Video2= clip2.set_audio(audio2)
    Video3= clip3.set_audio(audio3)
    Video_final = concatenate_videoclips([Video1,Video2,Video3])
    Video_final.write_videofile(f'Youtube Output/{output}.mp4',24)
    os.remove('audio1.mp3')
    os.remove('audio2.mp3')
    os.remove('audio3.mp3')
def create_short(img1,img2,img3,script='sort_script'):
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


    audio1 = AudioFileClip('audio1.mp3')
    audio2 = AudioFileClip('audio2.mp3')

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
    os.remove('audio1.mp3')
    os.remove('audio2.mp3')
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
    
