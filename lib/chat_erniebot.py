import lib.chat_erniebot as chat_erniebot
from baseconfig import erniebot_config
chat_erniebot.api_type = erniebot_config.api_type
chat_erniebot.access_token = erniebot_config.access_token

def chat(prompt):
     
    messages=[
        {"role": "user", "content": prompt}
    ]
    response = chat_erniebot.ChatCompletion.create(
                        model='ernie-4.0',
                        messages=messages,
                        top_p=0.95,
                        stream=False)
    content=response.get_result()
    return content