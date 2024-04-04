from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, vfx, VideoFileClip
import pyttsx3 
import os

def create_audio(script):
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
def create_video(frame_num):
    clips = []
    index = 1
    while index < frame_num:
        try:
            audio1 = AudioFileClip(f'Long form Videos/audios/audio{index}.mp3')
            image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
            clip1 = image1.set_duration(audio1.duration+0.5)
            Video1= clip1.set_audio(audio1)
        except:
            if index == 56: # No goal
                audio1 = AudioFileClip('Long form Videos/no-goal.mp3')
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
                audio1 = AudioFileClip('Long form Videos/goal.mp3')
                image1 = ImageClip(f'Long form Videos/Frames/{index}.png')
                clip1 = image1.set_duration(audio1.duration)
                Video1 = clip1.set_audio(audio1)
        clips += [Video1]
        index += 1
    
    Video_final = concatenate_videoclips(clips)
    Video_final.write_videofile('Long form Videos/video1.mp4',24)
def apendimage2video(path_video='Long form Videos/video1.mp4',path_image='Long form Videos/Frames/69.png',output='Long form Videos/video.mp4',img_duration=3):
    video1 = VideoFileClip(path_video)
    video2 = ImageClip(path_image).set_duration(img_duration)
    Video_final = concatenate_videoclips([video1,video2])
    Video_final.write_videofile(output,24)
    