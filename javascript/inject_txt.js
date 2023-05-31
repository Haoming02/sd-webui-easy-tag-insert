class LeInjector_TXT {
	static injectButton(button) {
		button.addEventListener('click', () => {
			const to_negative = document.getElementById('ez-tag-negative-txt')
			const checkbox = to_negative.querySelector('input[type=checkbox]')
			const id = checkbox.checked ? 'txt2img_neg_prompt' : 'txt2img_prompt'

			const textArea = gradioApp().getElementById(id).querySelector('textarea')

			var prompt = textArea.value.trim()

			if (prompt.includes(button.id)) {
				if (prompt.includes(', ' + button.id))
					prompt = prompt.replace(', ' + button.id, '')
				else if (prompt.includes(',' + button.id))
					prompt = prompt.replace(',' + button.id, '')
				else
					prompt = prompt.replace(button.id, '')
			}
			else {
				if (prompt.length == 0)
					prompt = button.id
				else if (prompt.slice(-1) == ',')
					prompt = prompt + ' ' + button.id
				else
					prompt = prompt + ', ' + button.id
			}

			textArea.value = prompt
			updateInput(textArea)
		})
	}

	static openButton(ez_container) {
		const button = document.getElementById('ez-tag-toggle-txt')
		const extraNetwork = document.getElementById('txt2img_extra_networks')
		const txt2imgActionColumn = document.getElementById('txt2img_tools').querySelector('.form')

		button.removeAttribute('id')
		button.removeAttribute('title')
		button.classList.add('tool')

		button.addEventListener('click', () => {
			if (extraNetwork.classList.contains('secondary-down'))
				extraNetwork.dispatchEvent(new Event('click'))

			this.isOn = !this.isOn
			ez_container.style.display = this.isOn ? 'block' : 'none'
		})

		extraNetwork.addEventListener('click',
			() => {
				if (ez_container.style.display != 'none')
					button.dispatchEvent(new Event('click'))
			}
		)

		const applyStyle = txt2imgActionColumn.children[3]
		txt2imgActionColumn.insertBefore(button, applyStyle)
	}

	static reconstructUI(dictionary) {

		const ez = document.getElementById('ez-tag-container-txt')
		const tabs = ez.querySelector('.tab-nav.scroll-hide')

		if (checkTabCount(Object.keys(dictionary).length, tabs.getElementsByTagName('button').length - 1))
			return;

		for (var key in dictionary) {
			let section = document.getElementById('tab-' + key.replace(/ /g, '-').toLowerCase() + '-txt')
			let buttons = section.getElementsByTagName('button')

			const dictKeys = Object.keys(dictionary[key]);
			const btnKeys = []

			for (let i = 0; i < buttons.length; i++)
				btnKeys[i] = buttons[i].innerText

			const toDelete = btnKeys.filter(x => !dictKeys.includes(x));
			const toAdd = dictKeys.filter(x => !btnKeys.includes(x));

			for (let i = 0; i < toAdd.length; i++) {
				let newBtn = buttons[0].cloneNode()
				newBtn.innerText = toAdd[i]
				LeInjector_TXT.injectButton(newBtn)
				section.querySelector('.gradio-row').append(newBtn)
			}

			for (let i = buttons.length - 1; i >= 0; i--) {
				for (let l = 0; l < toDelete.length; l++) {
					if (buttons[i].innerText == toDelete[l]) {
						buttons[i].remove()
						break;
					}
				}
			}

			buttons = section.getElementsByTagName('button')

			for (let i = 0; i < buttons.length; i++) {
				buttons[i].id = dictionary[key][buttons[i].innerText]
			}
		}
	}
}

onUiLoaded(async () => {
	const container = document.getElementById('txt2img_toprow')
	const ez = document.getElementById('ez-tag-container-txt')
	const tabs = ez.querySelector('.tab-nav.scroll-hide')

	container.after(ez)

	const refresh_btn = document.getElementById('ez-tag-refresh-txt')
	refresh_btn.addEventListener('click', () => {
		setTimeout(pollCollection, 250);
	})

	const to_negative = document.getElementById('ez-tag-negative-txt')
	to_negative.classList.remove('block')

	to_negative.style.margin = '0.3em';
	to_negative.style.marginLeft = '4'
	to_negative.style.marginRight = 0

	refresh_btn.style.margin = '0.3em';
	refresh_btn.style.marginLeft = 'auto'
	refresh_btn.style.marginRight = 0

	tabs.appendChild(refresh_btn)
	tabs.appendChild(to_negative)

	this.isOn = false
	ez.style.borderStyle = 'none'
	ez.style.display = 'none'

	const tabRows = ez.querySelectorAll('.tabitem')

	tabRows.forEach((tab) => {
		let buttons = tab.querySelectorAll("button")

		buttons.forEach((button) => {
			if (!button.id.includes('ez-tag')) {
				LeInjector_TXT.injectButton(button)
			}
		})
	})

	LeInjector_TXT.openButton(ez)
})