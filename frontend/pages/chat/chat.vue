<template>
  <view class="app-background">
    <view class="mobile-chat" >
		<!-- #ifndef MP-->
		<view :style="{'height': geStatusBarHeight() + 'px'}"></view>

        <uni-nav-bar 
		left-icon="arrow-left"
		@click-left="navigateBack"
		right-icon="redo-filled"
		@clickRight="showShare = true"
		color="#1989fa"
		fixed
		class="nav-bar"
		>
            <view class="nav-title" >
				<span :style="{ color: titleColor }">{{title}}</span>
			</view>
  
  
        </uni-nav-bar>
		 <!-- #endif -->
		 <!-- #ifdef MP-->
		  <view class="mp-nav-title" @click="openPopup">
		 	<span :style="{ color: titleColor }">{{title}}</span>
		 	<uni-icons v-if="showPopup"  type="arrow-down" size="13"></uni-icons>
		 	<uni-icons v-else type="arrow-up"  color="#1989fa"  size="13"></uni-icons>
		  </view>
		 		
		  <!-- #endif -->
		 
		<view class="chat-list-wrapper" ref="navBarRef" >
		 
			 
		  <view id="message-list-box" :style="{height: winHeight + 'px'}" class="message-list-box">
		    <scroll-view :scroll-top="scrollTop" scroll-y="true" 
		    			@scroll="" :style="{height: winHeight + 'px'}">
			<view class="scroll-content"
		     
		    >
			
		      <view v-for="item in chatData" :key="item" :border="false" class="message-line" @click="copy(item)">
		        <chat-prompt
		            v-if="item.type==='prompt'"
					
		            :content="item.content"
		            :created-at="dateFormat(item['created_at'])"
		            :icon="item.icon"
		            :model="model"
		            :tokens="item['tokens']"/>
		        <chat-reply v-else-if="item.type==='reply'" @click="copy(item.orgContent)"
		                    :content="item.content"
		                    :created-at="dateFormat(item['created_at'])"
		                    :icon="item.icon"
		                    :org-content="item.orgContent"
		                    :tokens="item['tokens']"/>
		      </view>
		    </view>
			 </scroll-view>
		  </view>
		</view>
		<view class="chat-box-wrapper" ref="bottomBarRef">
				  <view class="bt-icon" @click="inputVoice">
					  <uni-icons type="mic-filled" size="20"></uni-icons>
				  </view>
				  <view class="bt-input">
					  
				  	  <input confirm-type="search" @confirm="sendMessage" v-model="prompt" placeholder="请输入问题" placeholder-style="font-size:26rpx;color:rgba(203, 203, 203, 1);"></input>  
				  </view>
				  <view class="bt-btn">
				  	  <button size="small" type="primary" @click="sendMessage" >发送</button>
				  </view>
		</view>
		
		
	</view>
	
	<uni-popup ref="micPopup" type="bottom" @maskClick="micMaskClick">
		<view  :class="[transBack ? 'bg-black bg-opacity-50 flex flex-col justify-between items-center  w-screen h-screen pb-4' : 'bg-black flex flex-col justify-between items-center  w-screen h-screen pb-4']" >
		  <view class="flex flex-col items-center justify-center mt-10">
		     <h1 class="text-white mb-10">
		      小说AI
		     </h1>
		     <view class="bg-white rounded-full p-1">
		      <img @click="showBack" alt="" class="rounded-full" height="150" src="/static/images/avatar/gpt.png" width="150"/>
		     </view>
				 <view class="mt-10" style="width: 220px;">
				 		<video style="width: 220px;" v-show="activeCam" id="myVideo" autoplay ref="myVideo" src=""
				 				@error="videoErrorCallback" show-progress = false muted="true"></video>
				 </view>
		  </view>
	
			
			
		  <!-- Indicator -->
			<view class="mx-9" >
				<view class="flex flex-col items-center mb-8">
				 <view class="flex space-x-1 mb-4">
					<view :class="[activeMic ? 'indicator1' : 'indicator']">
					</view>
					<view :class="[activeMic ? 'indicator2' : 'indicator']">
					</view>
					<view :class="[activeMic ? 'indicator3' : 'indicator']" >
					</view>
				 </view>
				 <h2 class="text-white">
					{{activeMic ? '你可以开始说话' : '你已经静音'}}
				 </h2>
				</view>
				
				<!-- Control Buttons -->
				<view class="flex justify-center gap-x-10 w-screen items-center space-x-1">
				 <view class="flex flex-col items-center">
					<view :class="[activeMic ? 'bg-gray-800  p-2 rounded-full' : 'bg-white p-2 rounded-full']" @click="changeMic">
					 <uni-icons :color="[activeMic ? 'white' : 'red']" :type="[activeMic ? 'mic' : 'micoff-filled']" size="40" ></uni-icons>
					</view>
				 </view>
				 <view class="flex flex-col items-center">
					<view class="bg-red-600 p-2 rounded-full">
					 <uni-icons color="white" type="closeempty" size="40" @click="stopVoice"></uni-icons>
					</view>
				 </view>
				 <view class="flex flex-col items-center">
					<view :class="[activeCam ? 'bg-gray-800 p-2 rounded-full' : 'bg-white p-2 rounded-full']" @click="changeCam">
					 <uni-icons :color="[activeCam ? 'white' : 'red']" type="videocam-filled" size="40" ></uni-icons>
					</view>
				 </view>
				</view>
			</view>
			
		</view>
	</uni-popup>

	
	
	

  </view>
  
</template>

<script setup>
import {nextTick, onMounted, onUnmounted, ref} from "vue";
import {onBeforeRouteLeave, useRouter} from "vue-router";
import ChatPrompt from "@/components/chat/ChatPrompt.vue";
import ChatReply from "@/components/chat/ChatReply.vue";
import {dateFormat, processContent, randString, renderInputText, UUID, addClassToCodeTags} from "@/utils/libs";
import {geStatusBarHeight, getNavBarHeight} from "@/utils/system";
import { onShow, onHide,onLoad } from "@dcloudio/uni-app"
import {getChatConfig} from "@/store/chat";

import MarkdownIt from 'markdown-it';
import hl from 'highlight.js'
import 'highlight.js/styles/dark.css'
const winHeight = ref(0)
const navBarRef = ref(null)
const bottomBarRef = ref(null)
const router = useRouter()

const chatConfig = getChatConfig()
console.log('chatConfig',chatConfig)
const role = chatConfig.role
const model = chatConfig.model
const modelValue = chatConfig.modelValue
const title = chatConfig.title
const chatId = chatConfig.chatId
const usericon = chatConfig.icon
const showMic = ref(false)
const showPopup = ref(true)
const popupRef = ref(null)
const titleColor = ref("#333")

const chatData = ref([])
const loading = ref(false)
const finished = ref(false)
const error = ref(false)
const micPopup = ref("")
const scrollTop = ref(0)
const activeMic = ref(true)
const activeCam = ref(false)



const scroll = (e) => {
	console.log("scroll",e)
}
onMounted(async () => {
	let obj = uni.createSelectorQuery().select('.nav-bar')
	let navht = 0
	let bottomht = 0
    // #ifndef MP
	const data1 = await new Promise(resolve => {
		obj.boundingClientRect(resolve).exec()
	});
	navht = data1.height
	// #endif
	
	let obj2 = uni.createSelectorQuery().select('.chat-box-wrapper')
	const data2 = await new Promise(resolve => {
		obj2.boundingClientRect(resolve).exec()
	});
	bottomht=data2.height
	
	// #ifdef MP
	let mpht =0 
	let obj3 = uni.createSelectorQuery().select('.mp-nav-title')
	const data3 = await new Promise(resolve => {
		obj3.boundingClientRect(resolve).exec()
	});
	mpht = data3.height
	console.log("mpht:",mpht)
	navht = navht+mpht
	// #endif
	console.log("height:",navht,bottomht)

    winHeight.value = uni.getWindowInfo()['windowHeight']-navht-5 - bottomht
 
  
 
})



const copy = (item) => {
  console.log("setClipboardData",item)
  let value
  if(item.type=='prompt'){
	  value = item.content
  }else{
	  value = item.orgContent
  }
  uni.setClipboardData({
  	data: value,
  	success: function () {
  		uni.showToast({
  			title: "复制成功",
  			icon:'checkmarkempty'
  		});
  	}
  });


};



import latexPlugin from 'markdown-it-latex2img';
import mathjaxPlugin from 'markdown-it-mathjax';
const md = MarkdownIt({
  breaks: true,
    html: true,
    linkify: true,
    typographer: true,
    highlight: function (str, lang) {
	  console.log("")
      const codeIndex = parseInt(Date.now()) + Math.floor(Math.random() * 10000000)
      // 显示复制代码按钮
	  // 显示复制代码按钮
	      const copyBtn = `<span class="copy-code-mobile" data-clipboard-action="copy" data-clipboard-target="#copy-target-${codeIndex}">复制</span>
	  <textarea style="position: absolute;top: -9999px;left: -9999px;z-index: -9999;" id="copy-target-${codeIndex}">${str.replace(/<\/textarea>/g, '&lt;/textarea>')}</textarea>`
      // const copyBtn = `<span class="copy-code-mobile" copy-data-${codeIndex} style="z-index:20;" onclick="copyCode(${codeIndex})">复制</span>
      // <textarea style="position: absolute;top: -9999px;left: -9999px;z-index: -9999;" id="copy-target-${codeIndex}">${str.replace(/<\/textarea>/g, '&lt;/textarea>')}</textarea>`
      
	  if (lang && hl.getLanguage(lang)) {
        const langHtml = `<span class="lang-name">${lang}</span>`
		console.log("langHtml",langHtml)
        // 处理代码高亮
        const preCode = hl.highlight(lang, str, true).value
		console.log("preCode",preCode)
		// #ifdef MP
		return `<pre class="code-container hljs"><code class="language-python code-content hljs">${preCode}</code>${copyBtn} ${langHtml}</pre>`
		//#endif
        // 将代码包裹在 pre 中
        return `<pre class="code-container"><code class="language-python code-content hljs">${preCode}</code>${copyBtn} ${langHtml}</pre>`
      }
  
      // 处理代码高亮
      const preCode = md.utils.escapeHtml(str)
      // 将代码包裹在 pre 中
	  // #ifdef MP
      return `<pre class="code-container"><code class="language-python code-content hljs">${preCode}</code>${copyBtn}</pre>`
		//#endif
	  return `<pre class="code-container hljs"><code class="language-python code-content hljs">${preCode}</code>${copyBtn}</pre>`
	  
	}
});
md.use(latexPlugin)
md.use(mathjaxPlugin)



// 创建 socket 连接
const prompt = ref('');
const previousText = ref(''); // 上一次提问
const lineBuffer = ref(''); // 输出缓冲行
const activelyClose = ref(false); // 主动关闭
const canSend = ref(true);
const transBack = ref(false);


const disableInput = (force) => {
  canSend.value = false;
}

const enableInput = () => {
  canSend.value = true;
}

const showBack = () => {
  transBack.value = !transBack.value
}

// 将聊天框的滚动条滑动到最底部
const scrollListBox  = async () => {
	let obj2 = uni.createSelectorQuery().select('.scroll-content')
	const data2 = await new Promise(resolve => {
		obj2.boundingClientRect(resolve).exec()
	});
	console.log("scrollListBox",data2.height)
	scrollTop.value = data2.height+44
}

const sendMessage = () => {
  console.log("canSend",canSend.value )
  if (canSend.value === false) {
    //showToast("AI 正在作答中，请稍后...");
    return
  }

  if (prompt.value.trim().length === 0) {
    //showToast("请输入需要 AI 回答的问题")
    return false;
  }
  console.log("prompt",prompt.value )

  // 追加消息
  chatData.value.push({
    type: "prompt",
    id: randString(32),
    icon: '/static/images/avatar/user.png',
    content: renderInputText(prompt.value),
    created_at: new Date().getTime(),
  });

  nextTick(() => {
    scrollListBox()
  })

  disableInput(false)
  state.dc.send("Human:"+prompt.value)
  previousText.value = prompt.value;
  prompt.value = '';
  return true;
}


const buttonKeyPress= (event) => {
			console.log("event",event)
      // 检查按下的键是否是回车键
      if (event.keyCode === 13) {
        sendMessage();
      }
    }



const maskClick =()=>{
	console.log("maskClick",showPopup.value)
	if(showPopup.value){
		titleColor.value="#1989fa"
	}else{
		titleColor.value="#333"
	}
	showPopup.value=!showPopup.value
}	


const micMaskClick =()=>{
	console.log('语音识别结束');
	micPopup.value.close()
}	


const navigateBack=()=>{
  uni.$emit('refreshData', showPopup.value);
  uni.navigateBack(); // 返回上一个页面
}

// #ifdef WEB

const vocTitle = ref("未开始")
const text = ref("")
const partialResult = ref("...")
const result = ref("")
const valueWidth = ref("0px")
const myVideo = ref(null);


const inputVoice = () => {
  console.log('rtc开始11');
	state.stream.getTracks().forEach((track) =>{
	    console.log('语音识别开始11',track);
			if (track.kind ==='audio'){
				track.enabled = true
			}
			
	})
  micPopup.value.open()
	state.dc.send("start_recording")
	activeMic.value = true
	
}

const stopVoice = () => {
  console.log('rtc结束11');
	stopRtc()
  micPopup.value.close()
	state.dc.send("stop_recording")
}

const changeMic = () => {
	
  activeMic.value=!activeMic.value
	if(activeMic.value){
		state.stream.getTracks().forEach((track) =>{
		    console.log('语音识别开始11',track);
				if (track.kind ==='audio'){
					track.enabled = true
				}
				
		})
		state.dc.send("start_recording")
	}else{
		state.stream.getTracks().forEach((track) =>{
		    console.log('语音识别结束11',track);
				if (track.kind ==='audio'){
					track.enabled = false
				}
				
		})
		state.dc.send("stop_recording")
	}
}

const changeCam = () => {
  activeCam.value=!activeCam.value
	if(activeMic.value){
		state.stream.getTracks().forEach((track) =>{
		    console.log('语音识别开始11',track);
				if (track.kind ==='video'){
					track.enabled = true
				}
				
		})
		
	var video = document.querySelector("video");
			 // 旧的浏览器可能没有 srcObject
			 video.srcObject = state.stream;
			 video.onloadedmetadata = function (e) {
				 video.play();
			 };
			 
	}else{
		state.stream.getTracks().forEach((track) =>{
		    console.log('语音识别结束11',track);
				if (track.kind ==='video'){
					track.enabled = false
				}
				
		})
	}
}
// #endif



// webrtc 
let state = {
    pc:null,
    dc:null,
    stream:null,
}

onMounted(() => {
 startRtc()
});


const openPopup =()=>{
	console.log("open",showPopup.value)
	if(showPopup.value){
		popupRef.value.open();
		titleColor.value="#1989fa"
		popupRef.value.open();
	}else{
		titleColor.value="#333"
		popupRef.value.close();
	}
	showPopup.value=!showPopup.value
}	

function stopRtc(){
	state.stream.getTracks().forEach((track) =>{
	    track.enabled = false
			
	})
}

function startRtc() {
		console.log('start');
    const config = {
        sdpSemantics: 'unified-plan'
    };

    config.iceServers = [{ urls: ['stun:stun.l.google.com:19302'] }];

    state.pc = new RTCPeerConnection(config);
    state.pc.onconnectionstatechange = (ev) => {
        getcconnectionstatus()
    }
    state.dc = state.pc.createDataChannel("chat")
    state.dc.onopen = (ev) => {
        console.log("Data channel is open and ready to use");
        state.dc.send("Hello server");
    }
    state.dc.onmessage = (ev) => {
        console.log('Received message: ' + ev.data);
        if(ev.data === "ready") {
        }
        if(ev.data.startsWith("Human:") || ev.data.startsWith("AI:")) {
            let splits = ev.data.split(": ")
            if (splits.length > 1) {
                let messageText = splits.slice(1).join(": ")
                if (messageText) {
									
                    if (splits[0] === "AI") {
											if (messageText === 'start-response') {
											  chatData.value.push({
											    type: "reply",
											    id: randString(32),
											    icon: usericon,
											    content: ""
											  });
											} else if (messageText === 'end-response') { // 消息接收完毕
											  enableInput()
											  lineBuffer.value = ''; // 清空缓冲
											
											} else {
												
												lineBuffer.value += messageText;
												console.log('lineBuffer.value message: ' + lineBuffer.value);
												const reply = chatData.value[chatData.value.length - 1]
												reply['orgContent'] = lineBuffer.value;
												// reply['content'] = md.render(processContent(lineBuffer.value));
											  reply['content'] = lineBuffer.value;
												}
											} 
										if (splits[0] === "Human") {
											
											if (messageText === 'start-response') {
											  // 追加消息
											  chatData.value.push({
											    type: "prompt",
											    id: randString(32),
											    icon: usericon,
											    content: "",
											    created_at: new Date().getTime(),
											  });
											} else if (messageText === 'end-response') { // 消息接收完毕
											  enableInput()
											
											} else {
												const prompt = chatData.value[chatData.value.length - 1]
												prompt['content'] = renderInputText(messageText);
											
												}
                       
                    }
										nextTick(() => {
										  hl.configure({ignoreUnescapedHTML: true})
										  const lines = document.querySelectorAll('.message-line');
										  const blocks = lines[lines.length - 1].querySelectorAll('pre code');
										  blocks.forEach((block) => {
										    hl.highlightElement(block)
										  })
										  scrollListBox()
										
										  const items = document.querySelectorAll('.message-line')
										  const imgs = items[items.length - 1].querySelectorAll('img')
										  for (let i = 0; i < imgs.length; i++) {
										    if (!imgs[i].src) {
										      continue
										    }
										    imgs[i].addEventListener('click', (e) => {
										      e.stopPropagation()
										      showImagePreview([imgs[i].src]);
										    })
										  }
										})
                }
            }
						
        }
        if(ev.data.startsWith("playing:")) {
          
        }
    }
    state.dc.onclose = () => {
        console.log("Data channel is closed");
    }

    // connect audio / video
    state.pc.ontrack = (ev) => {
        console.log('Received remote stream',ev);
				var audio = new Audio();
				// 将音频元素的源设置为获取到的音频流
				audio.srcObject = ev.streams[0];
				// 播放音频
				audio.play();

    }
		
		getMedia()
}


function stop() {
    
    if(state.pc) {
        // close peer connection
        setTimeout(() => {
            state.pc.close();
            getcconnectionstatus()
            state = {pc:null, dc:null, stream:null}
        }, 500);
    }
}

function getMedia(){
	
    const constraints = {
        audio: true,
				video: {
				      width: { min: 1024, max: 1024 },
				      height: { min: 1024, max: 1024 }
				    }
    };
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(handleSuccess)
        .catch(handleFailure);
}



function handleSuccess(stream) {
	
    const tracks = stream.getTracks()
    console.log("Received: ", tracks.length, " tracks")
    state.stream = stream
    state.stream.getTracks().forEach((track) =>{
        state.pc.addTrack(track)
    })
		
		state.stream.getTracks().forEach((track) =>{
					track.enabled = false
		})
		// var video = document.querySelector("video");
		// 		 // 旧的浏览器可能没有 srcObject
		// 		 video.srcObject = stream;
		// 		 video.onloadedmetadata = function (e) {
		// 			 video.play();
		// 		 };
	 negotiate()
}


function handleFailure(error) {
    console.log('navigator.getUserMedia error: ', error);
}


function negotiate() {
    //pc.addTransceiver('audio', { direction: 'sendrecv' });
    return state.pc.createOffer().then((offer) => {
        return state.pc.setLocalDescription(offer);
    }).then(() => {
        // wait for ICE gathering to complete
        return new Promise((resolve) => {
            if (state.pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                const checkState = () => {
                    if (state.pc.iceGatheringState === 'complete') {
                        state.pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                };
                state.pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(() => {
			var offer = state.pc.localDescription;
			console.log("offer",offer)
			uni.request({
			    url: 'http://localhost:8089/offer', //仅为示例，并非真实接口地址。
			    data: {
                sdp: offer.sdp,
                type: offer.type,
          },
					method: 'POST',
			    header: {
			        'Content-Type': 'application/json'
			    },
			    success: (res) => {
			        console.log(res);
							state.pc.setRemoteDescription(res.data);
			    },
					fail: (res) => {
			        console.log("fail",res);
			    },
			});

       
    })
}

function getcconnectionstatus() {
    let status = "closed"
    if (state.pc) {
        status = state.pc.connectionState
    }
    console.log("getcconnectionstatus",status)
}


</script>

<style lang="stylus">
/deep/ .uni-navbar__header-container{
	justify-content: center
	.nav-title{
		display: flex
		align-items: center
	}
}

.indicator {
    width: 10px;
    height: 10px;
    background-color: #007bff;
    border-radius: 50%;
  }

.indicator1 {
    width: 10px;
    height: 10px;
    background-color: #007bff;
    border-radius: 50%;
    animation: wave 0.9s infinite;
  }
	
.indicator2 {
    width: 10px;
    height: 10px;
    background-color: #007bff;
    border-radius: 50%;
    animation: wave 0.6s infinite;
  }
	

.indicator3 {
    width: 10px;
    height: 10px;
    background-color: #007bff;
    border-radius: 50%;
    animation: wave 1.2s infinite;
  }
	
@keyframes wave {
    0% {
      transform: scale(1);
    }
    50% {
			height: 15px;
      transform: scale(1.4);
    }
    100% {
      transform: scale(1);
    }
  }

.mp-nav-title{
		display: flex
		justify-content: center
		position: fixed;
		left: 0;
		top: 0;
		align-items: center
		z-index: 200
		background-color: #FFF
		width: 100%
		margin-bottom: 10rpx
	}

/deep/ .uni-popup{
	/* #ifndef MP */
	margin-top: 88rpx
	/* #endif */
	/* #ifdef MP */
	margin-top: 44rpx
	position: absolute !important
	/* #endif */
	
}


.m-scroll{
	width: 100%;
	height: 100vh
}

.top-popup{
	height: 80%
	margin-top: 88rpx !important

	.top-popup-item{
		display: flex
		justify-content: space-between
		align-items: center
		padding: 20rpx 20rpx
		.pupup-title{
			color: #323233
			font-size: 28rpx
		}
		.pupup-detail{
			color: #969799
		}
		
	}
	.line{
		content: " ";
		margin: 0rpx 20rpx;
		border-bottom: 1px solid #969799;
		transform: scaleY(.2);
	}
}



@import "../../assets/css/mobile/chat-session.styl"
</style>