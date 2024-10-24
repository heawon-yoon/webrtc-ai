<template>
  <view class="mobile-message-prompt">
    <view class="chat-item">
      <view ref="contentRef" :data-clipboard-text="content" class="content" v-html="content"></view>
      <view class="triangle"></view>
    </view>

    <view class="chat-icon">
      <image src="/static/images/avatar/user.png" class="img"/>
    </view>
  </view>
  <view>
	<!-- 提示信息弹窗 -->
	<uni-popup ref="message" type="message">
		<uni-popup-message :type="msgType" :message="messageText" :duration="2000"></uni-popup-message>
	</uni-popup>
   </view>
</template>

<script setup>
import {onMounted, ref} from "vue";

const props = defineProps({
  content: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: '/images/user-icon.png',
  }
});
const contentRef = ref(null)
onMounted(() => {
  
})
</script>

<style lang="stylus">
.mobile-message-prompt {
  display flex
  justify-content: flex-end
  padding: 40rpx 5px 40rpx 40rpx;

  .chat-icon {
    margin-left 5px
    .img {
      width 32px;
	  height 32px;
    }
  }

  .chat-item {
    position: relative;
    padding: 0 5px 0 0;
    overflow: hidden;

    .triangle {
      width: 0;
      height: 0;
      border-top: 5px solid transparent;
      border-bottom: 5px solid transparent;
      border-left: 5px solid #98E165;
      position: absolute;
      right: 0;
      top: 10px;
    }

    .content {
      word-break break-word;
      text-align left
      padding: 5px 10px;
      background-color: #98E165;
      color #444444
      font-size: 14px
      border-radius: 5px
      line-height 1.5
    }
  }
}

.van-theme-dark {
  .mobile-message-prompt {
    .chat-item {

      .triangle {
        border-left: 5px solid #223A34
      }

      .content {
        background-color: #223A34
        color #c1c1c1
      }
    }
  }
}
</style>