
import json 

from moviepy.editor import *
from urllib import request

import os

from datetime import datetime

import re
 
def lyricTimeList(lyric):
    lyric =  re.sub(r'\[(\d+)\]', lambda x:   x.group(1) + '.', lyric)
    lyric=re.sub(r'\n\s*\n', '\n', lyric).strip()
    data=lyric.split('\n')
    processed_data = []

    # 遍历每一行数据
    for i in range(len(data) - 1):
        line = data[i]
        next_line = data[i + 1]
        
        # 提取 start 和 content
        start = int(line.split('.')[0])
        content = line.split('.')[1]
        
        # 使用下一行的开始作为当前行的结束
        end = int(next_line.split('.')[0])
        
        processed_data.append({"start": start, "end": end, "content": content})

    # 处理最后一行
    last_line = data[-1]
    last_start = int(last_line.split('.')[0])
    last_content = last_line.split('.')[1]
    last_end = last_start + 20

    processed_data.append({"start": last_start, "end": last_end, "content": last_content})
    return processed_data
 
   
def create_lyric_clip(text, start_time, duration,vheight):
    lyric_clip = (
        TextClip(text, fontsize=64, color='white', font='SimHei')
        .set_start(start_time)
        .set_duration(duration)
    )
    lyric_clip = lyric_clip.set_position(lambda t: ('center', vheight-160))
    return lyric_clip
      
def unionvideo(videoList,music='',lyric=''):
    print(videoList)
  
    
    video_files=[]
   
    i=0
    for v in videoList:
        file=videoList[i]
        video_files.append(VideoFileClip(file))
        i=i+1
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    mp4url = f"static/unionvideo_{timestamp}.mp4"
 
    
    final_clip = concatenate_videoclips(video_files)
    video_height = final_clip.h
 
    # 合成背景音乐
    if music!='':
        
        audio_clip = AudioFileClip(music)
        audio_clip.set_duration(min(audio_clip.duration,final_clip.duration))
        final_clip = final_clip.set_audio(audio_clip)
    # 添加歌词
    if lyric!='':
        lyric_clips = []
        lyricList=lyricTimeList(lyric)
        for row in lyricList:
            #print(row)
            lyric_clip = create_lyric_clip(row['content'], row['start'], row['end']-row["start"],video_height)
            lyric_clips.append(lyric_clip)
        final_clip = CompositeVideoClip([final_clip] + lyric_clips).set_duration(final_clip.duration)    
    final_clip.write_videofile(mp4url) 
    print(mp4url)
    return mp4url
def extract_video_urls(directory):
    video_list = []
    
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        # 检查是否为.txt文件
        if filename.endswith(".txt"):
            print(filename)
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                # 读取文件内容
                content = file.read()
                # 解析JSON数据
                data = json.loads(content)
                # 提取每个视频的videoURL
                videos = data.get('data', {}).get('videos', [])
                for video in videos:
                    video_url = video.get('videoURL')
                    if video_url:
                        video_list.append(video_url)
    
    return video_list
'''
videoList=extract_video_urls("./urls")
videoList.reverse()

for i in range(len(videoList)):
    request.urlretrieve(videoList[i], f"./music/{i}.mp4")
''' 

 
music='./music/music.mp3'
lyricFile='./music/lyric.txt'
mp4dir="./music"
videoList=[]
def get_sorted_mp4_files(directory):
    # 使用os.listdir获取指定目录下的所有文件和目录名
    files = os.listdir(directory)
    
    # 使用列表推导式筛选出所有的.mp4文件
    mp4_files = [file for file in files if file.endswith('.mp4')]
    
    # 定义一个用于排序的关键字函数，提取文件名中的数字部分并转为整数
    def sort_key(file_name):
        return int(file_name.split('.')[0])  # 提取文件名（去掉扩展名）并转为整数
    
    # 对mp4_files中的文件名按照数字大小进行排序
    sorted_mp4_files = sorted(mp4_files, key=sort_key)
    fileList=[]
    for i in range(len(sorted_mp4_files)):
        fileList.append(f"./music/{sorted_mp4_files[i]}")
         
     
    return fileList
 
videoList=get_sorted_mp4_files(mp4dir)

lyric=open(lyricFile,'r',encoding='utf-8').read()
result=unionvideo(videoList,music,lyric)   
print(result)

