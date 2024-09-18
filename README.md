# aimovie
 Using AI to generate short movie videos or music MVs   
 利用AI生成电影短视频或者音乐MV 
![](http://www.haicms.com/attach/git/text2movie.png) 
# 安装说明

默认接口依赖 

```
pip install moviepy requests gradio zhipuai dashscope
```

如果你要使用其他接口，请自行安装依赖
接口配置：
baseconfig.py
```
#chatglm开放平台 https://open.bigmodel.cn/
glm_api_key=''
#海螺开放平台 https://platform.minimaxi.com/
hailuo_config={
    "api_key":'',
    "group_id":'12'
}
#百度aistudio 文心一言 https://aistudio.baidu.com/
erniebot_config={
    "api_type":"aistudio",
    "access_token":"0c427760"
}
# 阿里云 dashscope https://dashscope.console.aliyun.com/
dashscope_config={
    "api_key":"sk-ada96"
}
apiFrom={
    "text2text":"zhipu",
    "text2video":"searchvideo",
    "tts":"tts_hailuo"
}
```

如果生成短片按照下面的提示词：  

帮我写一个有关七夕织女牛郎题材的短视频脚本，含3个场景，每个场景有一个详细的画面和旁白。
 


```
python text2movie_gradio.py 
```