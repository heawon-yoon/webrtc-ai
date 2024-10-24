[**English**](./README.md) | [**中文简体**](./README_zh.md)

# WEBRTC 实时音视频AI通话

毫秒级延迟webrtc音视频实时AI通话.
端到端本地模型

#### 技术特点


1. langchain技术支持Openai,ollama等常用大模型接口

2. webrtc底层毫秒级延迟,原生webrtc技术,易扩展跟集成

3. SST,TTS音频识别跟合成使用本地模型,流式合成

4. vad双重校验降噪及音频监听

5. 支持说话打断

6. 支持视频帧理解对话

7. 使用uniapp支持h5,小程序,app



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
打开.env文件配置openai key跟url
<br/>如果没有官方的可以使用这个代理[openai](https://api.xingyuntujiao.top)申请获取api_key
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



## 演示视频
demos on [bilibili](https://www.bilibili.com/video/BV1fjy6Y8ECM)   [youtube](https://youtu.be/4-svny5UPqg)
