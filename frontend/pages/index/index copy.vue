<template>
	<view class="app-background">
		
		<view class="content">
			<uni-search-bar v-model="chatName" placeholder="请输入会话标题" bgColor="#EEEEEE" @input="search" @clear="search" />
		<uni-search-bar v-model="chatName" placeholder="请输入会话标题" bgColor="#EEEEEE" @input="search" @clear="search" />
		
			
			<uni-list>
				<uni-list :border="true">
					<!-- 显示圆形头像 -->
					<block v-for="item in chats" :key="item.id">
						<uni-swipe-action-item>
							<uni-list-chat :avatar-circle="true" clickable
								
								:title="item.role_nm" 
								:avatar='"/static"+item.icon' 
								:note="item.title" 
								@click="toChat(item)"
								showSwitch
							>
							</uni-list-chat>
						<template #right>
						  <view class="btn">
							  <button square class = "btn"  type="primary" @click="editChat(item)">修改</button>
							  <button square class = "btn" type="warn" @click="removeChat(item)">删除</button>
						  </view>
						</template>
						</uni-swipe-action-item>
					</block>
					
					
				</uni-list>
			</uni-list>
			<view class="listtext" >没有更多了</view>
			
		</view>

		 
	</view>

</template>

<script setup>
import {
	ref,reactive, onMounted
} from "vue";
import {removeArrayItem} from "@/utils/libs";
import { onShow, onHide } from "@dcloudio/uni-app"

const title = ref("会话列表")
const chatName = ref("")
const chats = ref([])
const allChats = ref([])
const loading = ref(false)
const finished = ref(false)
const error = ref(false)
const loginUser = ref(null)
const isLogin = ref(false)
const roles = ref([])
const models = ref([])
const showPicker = ref(true)
const columns = ref([roles.value, models.value])

const showEditChat = ref(false)
const item = ref({})
const tmpChatTitle = ref("")
const popup = ref("")
const popupVal = ref([0,0])
const inputDialog = ref("")
function messageToggle(type) {  
	msgType.value = type  
	messageText.value = `这是一条${type}消息提示`  
	// this.$refs.message.open()  
	message.value.open()  
}  




const search = (e) => {
  if (e === '') {
    chats.value = allChats.value
    return
  }
  chatName.value = e
  const items = [];
  for (let i = 0; i < allChats.value.length; i++) {
    if (allChats.value[i].title.toLowerCase().indexOf(chatName.value.toLowerCase()) !== -1) {
      items.push(allChats.value[i]);
    }
  }
  chats.value = items;
}



const open =()=>{
	popup.value.open();
}	

const cancel_pop =()=>{
	popup.value.close();
}	

const confirm_pop =()=>{
	var jsonData = { role_id: roles.value[popupVal.value[0]], model_id: models.value[popupVal.value[1]],chat_id: 0};
	var jsonString = JSON.stringify(jsonData);
	console.log(jsonString)
	var encodedString = encodeURIComponent(jsonString);
	setChatConfig({
	    role: {
	      id: roles.value[popupVal.value[0]].value,
	      name: roles.value[popupVal.value[0]].text,
	      icon: roles.value[popupVal.value[0]].icon,
	      helloMsg: roles.value[popupVal.value[0]].helloMsg
	    },
	    model: roles.value[popupVal.value[1]].value,
	    modelValue: getModelValue(roles.value[popupVal.value[1]].value),
	    title: '新建会话',
	    chatId: 0
	  }) 
	// 使用navigateTo进行页面跳转，并附加参数
	uni.navigateTo({
	    url: '/pages/chat/chat?data=' + encodedString
	});
	popup.value.close();
}	



const toChat =(chat)=>{
	let role = {}
	for (let i = 0; i < roles.value.length; i++) {
	  if (roles.value[i].value === chat.role_id) {
	    role = roles.value[i]
	    break
	  }
	}
	setChatConfig({
	  role: {
	    id: chat.role_id,
	    name: role.text,
	    icon: role.icon
	  },
	  model: chat.model_id,
	  modelValue: getModelValue(chat.model_id),
	  title: chat.title,
	  chatId: chat.chat_id,
	  helloMsg: chat.hello_msg,
	})
	// 使用navigateTo进行页面跳转，并附加参数
	uni.navigateTo({
	    url: '/pages/chat/chat?chat_id=${chat.chat_id}'
	});
}	

const bindChange =(e)=>{
	const val = e.detail.value
	popupVal.value = val
	console.log(roles.value[popupVal.value[0]])
}	



const editChat = (row) => {
  inputDialog.value.open()
  item.value = row
  tmpChatTitle.value = row.title
}


const removeChat = (item) => {
    chats.value = removeArrayItem(chats.value, item, function (e1, e2) {
      return e1.id === e2.id
    })

}

 // 获取状态栏高度
const geStatusBarHeight= () => {
	return uni.getSystemInfoSync()['statusBarHeight']
}

// 获取导航栏高度
const getNavBarHeight= () => {
	// #ifdef MP-WEIXIN
	let menuButtonInfo = uni.getMenuButtonBoundingClientRect()
	// 导航栏高度 = 胶囊高度 + 上间距 + 下间距 + 微调	（menuButtonInfo.top - uni.getSystemInfoSync()['statusBarHeight'] = 上间距）	        
	let navbarHeight = menuButtonInfo.height + (menuButtonInfo.top - uni.getSystemInfoSync()['statusBarHeight']) * 2 + 2
	// #endif
	// #ifdef APP-PLUS || H5
	let navbarHeight = 44
	// #endif
	return navbarHeight
}
const uniWidth = ref(0)
// 获取导航栏高度
const getNavBarWidth= () => {
	console.log("navbarWidth")
	// #ifdef MP-WEIXIN
	let navbarWidth=uni.getMenuButtonBoundingClientRect().width
	// #endif
	// #ifdef APP-PLUS || H5
	let navbarWidth = 0
	// #endif
	console.log("navbarWidth",navbarWidth)
	uniWidth.value = navbarWidth
	return uni.getSystemInfoSync()['windowWidth']-navbarWidth
}


</script>

<style lang="stylus" scoped>

	
.content{
	.listtext{
		text-align: center
		color: #969799
		margin-top: 20rpx;
		font-size: 14px;
	}
	.btn{
		display: flex;
		justify-content: center;
		align-items: center;
		padding-right: 20rpx;
		height: 100%;
	}
}

.picker-view {
		width: 750rpx;
		height: 300rpx;
		margin-top: 5rpx;
	
	.item {
		line-height: 30rpx;
		text-align: center;
	}
}

.picker-head{
	display: flex;
	justify-content: space-between;
	align-items: center;
	.picker-left-btn{
		margin-left: 10rpx;
		border: none; 
		font-size: 28rpx;
		color: #969799;
	}
	.picker-right-btn{
		margin-right: 10rpx;
		border: none; 
		font-size: 28rpx;
		color: #1989fa
	}
	
}

.picker-option {
    display flex;
    width 100%;
    padding 0 10px;
    overflow hidden;
    height 40px;
    text-overflow ellipsis;
	text-align: center

    .img {
      width 20px;
      height 20px;
      margin-right 5px;
    }
  }

.popup{
	height: 600rpx;
}

</style>