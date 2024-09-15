import gradio as gr
from text2movie import text2movie

def text2movie_api(prompt,bgmusic):
    
    bgmusic2=[]
    print(bgmusic)
    if bgmusic==None:
        bgmusic2=[]
    else:    
        bgmusic2.append(bgmusic)  
    
    return text2movie(prompt,bgmusic2)

with gr.Blocks() as app:
    gr.Markdown("""
    # Text2Movie 一句话生成短片
    """)
    with gr.Row():
        with gr.Column():
            prompt=gr.Textbox(label="请输入要生成短片的文字",placeholder="请输入要生成短片的文字")
            audio=gr.Audio(label="请输入背景音乐",sources=["upload"],type="filepath")
        output=gr.Video(label="短片生成结果")
    btn=gr.Button("生成短片")
    btn.click(fn=text2movie_api,inputs=[prompt,audio],outputs=output)
app.launch()

