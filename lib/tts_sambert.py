# coding=utf-8

 
import dashscope
from dashscope.audio.tts import SpeechSynthesizer
from baseconfig import dashscope_config
from lib.basefun import uniqueName
dashscope.api_key = dashscope_config['api_key']

def tts(content,people=1):
    if people == 2:
        model='sambert-zhiqi-v1'
    else:
        model='sambert-zhichu-v1'    
    result = SpeechSynthesizer.call(model=model,
                                    text=content,
                                    sample_rate=48000,
                                    format='mp3')
    timestamp = uniqueName()
     
    filename = f"output/{timestamp}.mp3"
    if result.get_audio_data() is not None:
        with open(filename, 'wb') as f:
            f.write(result.get_audio_data())
        print('SUCCESS')
        return filename
    else:
        print('ERROR: response is %s' % (result.get_response()))
        return ''