[**English**](./README.md) | [**中文简体**](./README_zh.md)

# WEBRTC REAL_TIME AI

MS delays webrtc audio and video real-time AI calls.
End-to-end local model

#### Skills


1. Langchain technology supports Openai,ollama and other common large model interfaces

2. Webrtc underlying millisecond latency,Native webrtc technology, easy to expand and integrate

3. SST,TTS audio recognition and synthesis using local models,Streaming synthesis

4. Vad double check noise reduction and audio monitoring

5. Supportive interruption

6. Supports video frame understanding dialog

7. Support h5, mini program, apps with uniapp



## Installation
### STEP 1
```
git clone https://github.com/heawon-yoon/webrtc-ai.git
```

### STEP 2 Backend
tested with python3.10

```
cd backend
conda create -n webrtcai python=3.10 -y
conda activate webrtcai
pip install -r requirements.txt
python server.py
```
#### NOTE 
need to set the openai key and url from .evn file
<br/>如果没有官方的可以使用这个代理[openai](https://api.xingyuntujiao.top) 申请获取api_key
  没有访问限制,超级优惠,2人民币=1美元
```
OPENAI_API_BASE=https://api.xingyuntujiao.top/v1
OPENAI_API_KEY=XXXX
```


### STEP 3 FrontEnd
using uniapp,vue3
```
cd frontend
npm install -g @vue/cli
npm install
```

打开Hbuilder工具导入frontend项目.
选择运行到浏览器



## DEMO VIEDEO
demos on [bilibili](https://www.bilibili.com/video/BV1fjy6Y8ECM)   [youtube](https://youtu.be/4-svny5UPqg)
