<template>
  <view class="mobile-message-reply">
    <view class="chat-icon">
      <image :src="icon" class="img"/>
    </view>

    <view class="chat-item">
      <view class="triangle"></view>
      <view class="content-box" ref="contentRef">
        <view class="content content-mobile" data-clipboard-action="copy" v-html="content">
		</view>
      </view>

    </view>
  </view>
</template>

<script setup>
import {nextTick, onMounted, ref} from "vue"


const props = defineProps({
  content: {
    type: String,
    default: '',
  },
  orgContent: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: '/static/images/avatar/gpt.png',
  }
});

const contentRef = ref(null)
onMounted(() => {

})
</script>

<style lang="stylus">
 .p-code {
            color #2b2b2b
            background-color #c1c1c1 !important
            padding 2px 5px
            border-radius 5px
          }
.mobile-message-reply {
  display flex
  justify-content: flex-start;
  padding: 0px 5px 0px 5px

  .chat-icon {
    margin-right 5px

    image {
      width 32px
	  height: 32px
      img {
        border-radius 5px
      }
    }
  }

  .chat-item {
    display: inline-block;
    position: relative;
    padding: 0 0 0 5px;
    overflow: hidden;

    .triangle {
      width: 0;
      height: 0;
      border-top: 5px solid transparent;
      border-bottom: 5px solid transparent;
      border-right: 5px solid #fff;
      position: absolute;
      left: 0;
      top: 13px;
    }

    .content-box {

      display flex
      flex-direction row

      .content {
        text-align left
        width 100%
        overflow-x auto
        min-height 20px;
        word-break break-word;
        padding: 5px 10px;
        color #444444
        background-color: #ffffff;
        font-size: 14px
        border-radius: 5px;

        p:last-child {
          margin-bottom: 0
        }

        p:first-child {
          margin-top 0
        }

        p {
          .abc {
            color #2b2b2b
            background-color #c1c1c1 !important
            padding 2px 5px
            border-radius 5px
          }

          img {
            max-width 100%
          }
        }
		
        

        .lang-name {
          display none
          position absolute;
          right 10px
          bottom 50px
          padding 2px 6px 4px 6px
          background-color #444444
          border-radius 10px
          color #00e0e0
        }


        // 设置表格边框

        table {
          width 100%
          margin-bottom 1rem
          color #212529
          border-collapse collapse;
          border 1px solid #dee2e6;
          background-color #ffffff

          thead {
            th {
              border 1px solid #dee2e6
              vertical-align: bottom
              border-bottom: 2px solid #dee2e6
              padding 10px
            }
          }

          td {
            border 1px solid #dee2e6
            padding 10px
          }
        }

        // 代码快

        blockquote {
          margin 0
          background-color: #ebfffe;
          padding: 0.8rem 1.5rem;
          border-left: 0.5rem solid;
          border-color: #026863;
          color: #2c3e50;
        }
      }
    }

  }
}


.van-theme-dark {
  .mobile-message-reply {
    .chat-item {
      .triangle {
        border-right: 5px solid #404042;
      }

      .content-box {
        .content {
          color #c1c1c1
          background-color: #404042;

          p > code {
            color #c1c1c1
            background-color #2b2b2b
          }
        }
      }

    }
  }

}
.code-container {
	  position relative
	  /* #ifdef MP */
	  background-color: black
	  border-radius: 20rpx
	   padding: 30rpx
	   line-height: 1.5
	  /* #endif */
	
	.hljs {
			border-radius 10px
			line-height 1.5
	}
	.code-content{
			  //margin:35rpx
	}
	
	.copy-code-mobile {
			position: absolute;
			right 10px
			top 10px
			cursor pointer
			font-size 12px
			color #c1c1c1
	
			&:hover {
			  color #20a0ff
			}
	}

}
</style>