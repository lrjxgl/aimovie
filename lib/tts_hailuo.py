import json
import requests
from baseconfig import hailuo_config
from lib.basefun import uniqueName
import binascii
def tts(content='',people=''):
    group_id=hailuo_config["group_id"]
    url = "https://api.minimax.chat/v1/t2a_v2?GroupId="+group_id
    api_key=hailuo_config["api_key"]
    if people == 2:
        
        voice_id='female-shaonv'
    else:
        voice_id='male-qn-qingse'
    payload = json.dumps({
        "model": 'speech-01-turbo',
        "text": content,
        "stream": False,
        
        "voice_setting":{
            "voice_id": voice_id,
            "speed": 1,
            "vol": 1,
            "pitch": 0
        },
        "audio_setting":{
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3"
        }
    })
    headers = {
        'authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res=response.json()
    #print(res)
    hex_string=res['data']['audio']
    byte_array = binascii.unhexlify(hex_string)
    
    # 写入到MP3文件中
    output_file="output/audio/"+uniqueName()+'.mp3'
    with open(output_file, 'wb') as f:
        f.write(byte_array)
    #print("语音合成成功")
    #print(output_file)
    return output_file

