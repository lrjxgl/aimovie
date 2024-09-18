import serviceConf
import requests
import os
def upload_file(file_path):
    if os.path.exists(file_path)==False:
        return ''
    url=serviceConf.apiHost+"/module.php/aiapi_upload/auth"
    url=serviceConf.apiHost+"/index.php/ossupload/auth"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
        cfg=response.json()
        #print(cfg)
        
        fdata={
           
            "OSSAccessKeyId":cfg['accessid'],
            "policy":cfg['policy'],
            "Signature":cfg['sign'],
            "key":cfg['key'] + os.path.basename(file_path),
            "callback":cfg['callback'],
        }
        
        # 定义文件以二进制形式打开
        with open(file_path, 'rb') as file:
            # 使用files参数而不是data参数来发送文件
        
            fdata['file'] = (os.path.basename(file_path), file)
            
            response = requests.post(cfg['url'],files=fdata, allow_redirects=True)
            if response.status_code == 200:
                print(response.text)
                res=response.json()
                return res['filename']
            else:
                print(response.text)
    else:
        print(response.text)
        return ''    
    

    return ''