<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

// 在项目下的App.vue增加如下css代码
<style lang="scss">
	@import 'tailwindcss/base';
	@import 'tailwindcss/utilities';
	@import 'tailwindcss/components';
	
.app-background{
	width: 100%;
}
</style>
