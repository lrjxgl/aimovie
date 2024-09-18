import gradio as gr
import re
import json 
 
import math
from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip 
import numpy as np 
from datetime import datetime 


from lib.searchvideo import text2video
from lib.tts_hailuo import tts
def parseDuibai(text):
    pattern = r'\[(\d+)\|(\d+)\](.*)'

    # 使用findall或search方法来查找所有匹配项
    matches = re.findall(pattern, text)
    
    # 创建一个空列表来存储结果
    result = []

    # 遍历所有匹配项并构造字典
    for match in matches:
        # 提取匹配的信息
        start = int(match[0])
        people = int(match[1])
        content = match[2].strip()  # 去除两端空白字符

        # 构造字典并添加到结果列表中
        result.append({'start': start, 'content': content, 'people': people})
    print(result)
    return result
def text2movie_api(sences,duibais,bgmusic2):
    
    bgmusic=[]
    print(bgmusic2)
    if bgmusic2==None:
        bgmusic=[]
    else:    
        bgmusic.append(bgmusic2)  
    
    senceList=sences.split('\n')
   
    duibaiList=parseDuibai(duibais)
   
    videoList=[]
   
    #demo
 
    for i in range(len(senceList)):
        video=text2video(senceList[i])
        videoList.append(video)
            
   
    print(videoList)
    
    

    # 生成旁白
    print("生成旁白")
    
    audioList=[]
    print(duibaiList)
    for p in duibaiList:
         
        audio=tts(p["content"],p["people"])
        audioList.append({
            'start': p["start"],
            'content': p["content"],
            'audio':audio
        })
  
    

    # 合并视频音频
   
    
    mp4url= unionvideo(videoList,audioList,bgmusic)  
    print(mp4url)
    print("视频合成成功")  
    return mp4url  

def merge_audio_clips(audios, output_path=''):
    # 创建空的 CompositeAudioClip 对象作为容器
    final_clip = None
    audio_files=[]
    start_times=[]
    for audio in audios:
        audio_files.append(audio['audio'])
        start_times.append(audio['start'])
    # 遍历所有音频文件
    for audio_file, start_time in zip(audio_files, start_times):
        # 加载音频文件
        clip = AudioFileClip(audio_file)
        
        # 如果不是第一个音频文件，则需要创建一个新的 CompositeAudioClip 并设置开始时间
        if final_clip is None:
            final_clip = clip
        else:
            # 创建一个空的静音片段来填补时间差
            silence_duration = start_time - final_clip.duration
            
            sampling_rate = 44100  # 采样率为44.1kHz

            # 生成一个全零数组作为静音数据
            audio_data = np.zeros((int(silence_duration * sampling_rate), 2), dtype=np.float32)

            # 使用AudioArrayClip创建音频剪辑
            silence = AudioArrayClip(audio_data, fps=sampling_rate)
            
            
            # 将当前音频片段连接到最终音频片段上
            final_clip = concatenate_audioclips([final_clip, silence, clip])
    
    # 导出最终的音频文件
    #final_clip.write_audiofile(output_path)
    return final_clip

def unionvideo(videoList,audioList,bgmusic=[]):
    print(videoList)
    print(audioList)
    
    video_files=[]
    audioClips=[]
    i=0
    for v in videoList:
        file=videoList[i]
        video_files.append(VideoFileClip(file))
        i=i+1
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    mp4url = f"static/unionvideo_{timestamp}.mp4"
 
    
    
    final_clip = concatenate_videoclips(video_files)
    
    # 合成语音
    if len(audioList)>0:

        concatenated_audio=merge_audio_clips(audioList)
        final_clip = final_clip.set_audio(concatenated_audio)
    # 合成背景音乐
    if len(bgmusic)>0:
        msaudioClips=[]
        for i in range(len(bgmusic)):
            file=bgmusic[i]      
            msaudioClips.append(AudioFileClip(file))
        concatenated_audio = concatenate_audioclips(msaudioClips)
        audio_clip = concatenated_audio.set_duration(final_clip.duration)
        if len(audioList)>0:    
            # 将音频音量降低一些，使背景音乐不会盖过原声
            audio_clip = audio_clip.volumex(0.5)  # 可根据需要调整音量大小

            # 合并原有音频和背景音乐
            final_audio = CompositeAudioClip([final_clip.audio, audio_clip])

            # 设置视频的音频为最终的音频
            final_clip = final_clip.set_audio(final_audio)
        else:
            final_clip = final_clip.set_audio(audio_clip)
 
    final_clip.write_videofile(mp4url) 
    print(mp4url)
  
    return mp4url

with gr.Blocks() as app:
    gr.Markdown("""
    # Text2Movie 手写场景和对白生成短片
    """)
    with gr.Row():
        with gr.Column():
            sences=gr.Textbox(label="请输入短片场景",placeholder="请输入短片场景，每行一个",lines=20)
        with gr.Column():
            duibais=gr.Textbox(label="请输入对白",placeholder="请输入对白，每行一个",lines=10)
            audio=gr.Audio(label="请输入背景音乐",sources=["upload"],type="filepath")
    output=gr.Video(label="短片生成结果")
    btn=gr.Button("生成短片")
    btn.click(fn=text2movie_api,inputs=[sences,duibais,audio],outputs=output)
app.launch()

