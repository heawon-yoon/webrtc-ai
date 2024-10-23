const path = require("path");

const resolve = (p) => {
  return path.resolve(__dirname, p);
};
/** @type {import('tailwindcss').Config} */
module.exports = {
	// 增加前辍避免样式冲突
  // 注意此处，一定要 `path.resolve` 一下, 传入绝对路径
  // 你要有其他目录，比如 components，也必须在这里，添加一下
  content: [
	  "./index.html", 
	  "./pages/**/*.{html,js,ts,jsx,tsx,vue}",
	  "./components/**/*.{html,js,ts,jsx,tsx,vue}"
  ].map(resolve),
  corePlugins: {
    // 跨多端可以 h5 开启，小程序关闭
    preflight: false,
  },
};
