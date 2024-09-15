import serviceConf
import requests
import os
def upload_file(file_path):
    
    if os.path.exists(file_path)==False:
        return ''
    
    url=serviceConf.apiHost+"/mm/aiapi_upload/upload"
    fdata={          
        "appid":"appid"
    }
    files = {
        'file': (file_path, open(file_path, 'rb')),
    }
    data = {
        'key': 'value',
    }
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print(response.text)
        res=response.json()
        
        return res['fileurl']
    else:
        print(response)   
    return ''