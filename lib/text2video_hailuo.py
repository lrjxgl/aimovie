import json
 
import time
import requests
from datetime import datetime
import os
from baseconfig import hailuo_api_key
def createTask(prompt='',imgurl=''):
    url = "https://api.minimax.chat/v1/video_generation"
    api_key=hailuo_api_key

    payload = json.dumps({
        "model": "video-01", 
        "prompt": prompt,
    })
    headers = {
        'authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res=response.json()
    print(res)
    with open("./log/text2video_hailuo.txt", "a", encoding="utf-8") as fp:
            fp.write(str(res["task_id"]) + "\n")
    return res["task_id"]

def checkTask(id):
    api_key=hailuo_api_key
    while(True):
       
        task_id=id

        url = f"http://api.minimax.chat/v1/query/video_generation?task_id={task_id}"

        payload = {}
        headers = {
            'authorization': f'Bearer {api_key}',
            'content-type': 'application/json',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        res=response.json()
        #print(res) 
        if res["status"]=='Success':
            
             
            mp4url=download(res["file_id"])
            imgurl='' 
            
            print('success')
            return [mp4url,imgurl]
            break
        elif res["status"]=='Failed':
            print('fail') 
            return ['','']
        else:
            print('doing')
        time.sleep(3)  

def download(file_id):
    # 发起 GET 请求获取视频数据
    api_key=hailuo_api_key
    url = "https://api.minimax.chat/v1/files/retrieve?file_id="+file_id
    headers = {
        'authorization': 'Bearer '+api_key,
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)

    url = response.json()['file']['download_url']

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_filename = os.path.basename(url)
    filename = f"output/{timestamp}.mp4"
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)
        print("视频下载完成.")
        return filename  
     
def text2video(prompt='',imgurl=''):
    
    id=createTask(prompt=prompt,imgurl=imgurl)
    #id='1726380590156'
    mp4url,imgurl=checkTask(id) 
     
    return mp4url