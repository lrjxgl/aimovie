 
import re
import json 
 
import math
from moviepy.editor import *
 
 
from datetime import datetime 
from lib.chat_zhipu import chat
from lib.text2video_zhipu import text2video
from lib.tts_sambert import tts
 
 
 
def text2movie(prompt,bgmusic=[]):
    duibaiList =[]
    senceList=[]
    content=""
    while True: 
        content=chat(prompt) 
        print(content)
        #content=testContent
        content=content.replace("“","").replace("”","").replace(":","：").replace("旁白：\n","旁白：")
        pattern2 = re.compile(r'旁白[^：]*：(.*)', re.I)
        duibaiList = pattern2.findall(content)
       
        pattern = r"画面[^：]*：(.*?)旁白："
        senceList = re.findall(pattern, content, re.I | re.S)
        

        # 检查两个匹配结果的长度是否相同，如果不同或者为0，返回错误信息
        if len(senceList) != len(duibaiList) or len(senceList) == 0:
            print(prompt)
            print(json.dumps({"error": 1, "message": "text2text生成错误"}))
            continue
        break
    #print(senceList)
    #print(duibaiList)
    
    # 生成视频
    print("生成视频")
    videoList=[]
    vsenceList=[]
    #demo
    videoNum=0
    for i in range(len(senceList)):
        #语音1秒6个字 一个视频6秒
        m=math.ceil(len(duibaiList[i])/28)
    
        for j in range(m):
            videoNum=videoNum+1
            vsenceList.append(senceList[i])
            video=text2video(senceList[i])
            videoList.append(video)
           
    print(videoNum)
   
    print(videoList)
    
    

    # 生成旁白
    print("生成旁白")
    
    audioList=[]
     
    for p in duibaiList:
        print(p)
        audio=tts(p)
        audioList.append(audio)
  
    

    # 合并视频音频
   
    
    mp4url= unionvideo(videoList,audioList,bgmusic)  
    print(mp4url)
    print("视频合成成功")  
      
   

      
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
        i=0
        for v in audioList:
            file=audioList[i]
        
            audioClips.append(AudioFileClip(file))
            i=i+1
        #video_clip = VideoFileClip(mp4url)
        concatenated_audio = concatenate_audioclips(audioClips)
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

if __name__ == "__main__":

    #bgmusic=['output/bg.mp3']   
    result=text2movie("帮我写一个有关七夕织女牛郎题材的短视频脚本，含3个场景，每个场景有一个详细的画面和旁白。")   
    print(result)



