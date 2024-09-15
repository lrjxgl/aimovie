import os
import random
def pick_random_video(directory):
    # 获取指定目录下的所有文件名
    files = os.listdir(directory)
    
    # 过滤出视频文件（这里定义了一些常见的视频扩展名）
    video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv')
    videos = [file for file in files if file.endswith(video_extensions)]
    
    # 检查是否找到了视频文件
    if not videos:
        print("没有找到任何视频文件。")
        return None
    
    # 随机选取一个视频文件
    selected_video = random.choice(videos)
    return os.path.join(directory, selected_video)
def text2video(prompt='',imgurl=''):
    mp4url=pick_random_video('searchvideos')
    return mp4url

def img2video(prompt='',imgurl=''):
    mp4url=pick_random_video('output')
    return mp4url