import {randString} from "@/utils/libs";

/**
 * storage handler
 */

const UserTokenKey = "Hunkun_AI_Authorization";
const AdminTokenKey = "Hunkun_AI_Admin-Authorization"

export function getSessionId() {
    return randString(42)
}

export function getUserToken() {
	return uni.getStorageSync(UserTokenKey)
}

export function setUserToken(token) {
	uni.setStorageSync(UserTokenKey, token)
}

export function removeUserToken() {
	uni.removeStorage({
		key: UserTokenKey,
		success: function (res) {
			console.log('success');
		}
	});
}

export function getAdminToken() {
    return ""
}

export function setAdminToken(token) {
    
}

export function removeAdminToken() {
}
