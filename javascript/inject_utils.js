class injectUtils {
	static TXT2IMG = 0
	static IMG2IMG = 1
	static Modes = ['txt', 'img']

	static getToprows() { return [document.getElementById('txt2img_toprow'), document.getElementById('img2img_toprow')] }
	static getContainers() { return [document.getElementById('ez-tag-container-txt'), document.getElementById('ez-tag-container-img')] }
	static getTabNavs(containers) { return [containers[this.TXT2IMG].querySelector('.tab-nav.scroll-hide'), containers[this.IMG2IMG].querySelector('.tab-nav.scroll-hide')] }
	static getRefreshs() { return [document.getElementById('ez-tag-refresh-txt'), document.getElementById('ez-tag-refresh-img')] }
	static getToNegs() { return [document.getElementById('ez-tag-negative-txt'), document.getElementById('ez-tag-negative-img')] }
	static getTabRows(containers) { return [containers[this.TXT2IMG].querySelectorAll('.tabitem'), containers[this.IMG2IMG].querySelectorAll('.tabitem')] }
}