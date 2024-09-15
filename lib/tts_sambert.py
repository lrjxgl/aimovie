# coding=utf-8

import sys
from datetime import datetime
import dashscope
from dashscope.audio.tts import SpeechSynthesizer
from baseconfig import dashscope_config

dashscope.api_key = dashscope_config['api_key']

def tts(content):

    result = SpeechSynthesizer.call(model='sambert-zhichu-v1',
                                    text=content,
                                    sample_rate=48000,
                                    format='mp3')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
     
    filename = f"output/{timestamp}.mp3"
    if result.get_audio_data() is not None:
        with open(filename, 'wb') as f:
            f.write(result.get_audio_data())
        print('SUCCESS')
        return filename
    else:
        print('ERROR: response is %s' % (result.get_response()))
        return ''