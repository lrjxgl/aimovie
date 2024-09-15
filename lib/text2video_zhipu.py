from zhipuai import ZhipuAI
import baseconfig
import time
import requests
from datetime import datetime
import os
client = ZhipuAI(api_key=baseconfig.glm_api_key)  
def createTask(prompt='',imgurl=''):
    response = client.videos.generations(
        model="cogvideox",
        prompt=prompt,
        image_url=imgurl
    )
    print(response)
    with open("./log/text2video_zhipu.txt", "a", encoding="utf-8") as fp:
            fp.write(str(response.id) + "\n")
    return response.id

def checkTask(id):
    while(True):
        res = client.videos.retrieve_videos_result(
            id=id
        )
        #print(res) 
        if res.task_status=='SUCCESS':
            
            mp4url=res.video_result[0].url
            mp4url=download(mp4url)
            imgurl=res.video_result[0].cover_image_url
            imgurl=download(imgurl)
            
            print('success')
            return [mp4url,imgurl]
            break
        elif res.task_status=='FAIL':
            print('fail') 
            return ['','']
        else:
            print('doing')
        time.sleep(3)  

def download(url):
    # 发起 GET 请求获取视频数据
    response = requests.get(url, stream=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_filename = os.path.basename(url)
    filename = f"output/{timestamp}_{original_filename}"
    # 检查请求是否成功
    if response.status_code == 200:
        # 打开一个文件，以二进制写模式 ('wb')
        with open(filename, 'wb') as file:
            # 写入视频数据到文件
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("视频下载完成.")
        return filename
    else:
        print("无法下载视频.")
    return '' 
def text2video(prompt='',imgurl=''):
    
    id=createTask(prompt=prompt,imgurl=imgurl)
    mp4url,imgurl=checkTask(id) 
     
    return mp4url