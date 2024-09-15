from zhipuai import ZhipuAI
import baseconfig
def chat(prompt):
    client = ZhipuAI(api_key=baseconfig.glm_api_key)  
    response = client.chat.completions.create(
        model="glm-4-flash",   
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content