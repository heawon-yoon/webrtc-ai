<template>
	<view class="app-background">
		
		<view class="content">
			<uni-search-bar v-model="chatName" placeholder="请输入会话标题" bgColor="#EEEEEE" @input="search" @clear="search" />
		
			
			<uni-list>
				<uni-list :border="true">
					
					<!-- 显示圆形头像 -->
					<block v-for="item in chats" :key="item.id">
						
							<uni-list-chat :avatar-circle="true" clickable
								
								:title="item.title" 
								:avatar='item.icon' 
								:note="item.role_nm" 
								@click="toChat(item)"
								showSwitch
							>
							</uni-list-chat>
					
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
import {setChatConfig} from "@/store/chat";

const title = ref("会话列表")
const chatName = ref("")
const chats = ref([])
const allChats = ref([])



onShow(() => {
	console.log("index onMounted")
		chats.value = [{
			id: "1",
			title: "小说AI",
			icon: '/static/images/avatar/gpt.png',
			role_nm: "小说主人公主动跟你聊天", 
		},
		{
			id: "2",
			title: "英语陪练",
			icon: '/static/images/avatar/gpt.png',
			role_nm: "英语陪练", 
		}
		]
		
		allChats.value = chats.value

})

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




const toChat =(chat)=>{
	console.log("chat",chat)
	
	setChatConfig({
	    model: chat.role_nm,
	    title: chat.title,
	    chatId: chat.id,
			icon:chat.icon
	  }) 
	// 使用navigateTo进行页面跳转，并附加参数
	uni.navigateTo({
	    url: '/pages/chat/chat?chat_id=${chat.id}'
	});
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


</style>