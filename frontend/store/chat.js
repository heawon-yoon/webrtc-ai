const CHAT_CONFIG_KEY = "Hunkun_AI_chat_config"

export function getChatConfig() {
	return uni.getStorageSync(CHAT_CONFIG_KEY)
}

export function setChatConfig(chatConfig) {
	uni.setStorageSync(CHAT_CONFIG_KEY, chatConfig)
}