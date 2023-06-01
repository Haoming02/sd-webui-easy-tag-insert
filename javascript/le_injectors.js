class le_Injector {

	constructor() {
		this.toprows = injectUtil.getToprows();
		this.ez_containers = injectUtil.getContainers();
		this.tabs = injectUtil.getTabs(this.ez_containers);
		this.refresh_btns = injectUtil.getRefresh();
		this.to_negatives = injectUtil.getToNeg();
		this.tabRows = injectUtil.getTabRows(this.ez_containers);
		this.isOns = [false, false]
	}

	injectButton(button, index) {
		const mode = injectUtil.Modes[index]

		button.addEventListener('click', () => {
			const checkbox = this.to_negatives[index].querySelector('input[type=checkbox]')
			const id = checkbox.checked ? mode + '2img_neg_prompt' : mode + '2img_prompt'
			const textArea = gradioApp().getElementById(id).querySelector('textarea')

			let prompt = textArea.value.trim()

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

	pollCollection = () => {
		const dummy = document.getElementById('ez-tag-textbox').querySelector('textarea')
		if (dummy.value.length < 1) { setTimeout(this.pollCollection, 100) }

		else {
			const dictionary = JSON.parse(dummy.value.replace(/'/g, '"'));

			this.reconstructUI(dictionary)
		}
	}

	reconstructUI(dictionary) {
		for (let index = injectUtil.TXT2IMG; index <= injectUtil.IMG2IMG; index++) {

			const mode = injectUtil.Modes[index]

			if (injectUtil.checkTabCount(Object.keys(dictionary).length, this.tabs[index].getElementsByTagName('button').length - 1))
				return;

			for (var key in dictionary) {
				let section = document.getElementById('tab-' + key.replace(/ /g, '-').toLowerCase() + '-' + mode)
				let buttons = section.getElementsByTagName('button')

				const dictKeys = Object.keys(dictionary[key])
				const btnKeys = []

				for (let i = 0; i < buttons.length; i++)
					btnKeys[i] = buttons[i].innerText

				const toDelete = btnKeys.filter(x => !dictKeys.includes(x))
				const toAdd = dictKeys.filter(x => !btnKeys.includes(x))

				for (let i = 0; i < toAdd.length; i++) {
					let newBtn = buttons[0].cloneNode()
					newBtn.innerText = toAdd[i]
					this.injectButton(newBtn, index)
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

				for (let i = 0; i < buttons.length; i++)
					buttons[i].id = dictionary[key][buttons[i].innerText]
			}

		}
	}

	openButton(index) {
		const mode = injectUtil.Modes[index]

		const button = document.getElementById('ez-tag-toggle-' + mode)
		const extraNetwork = document.getElementById(mode + '2img_extra_networks')
		const actionColumn = document.getElementById(mode + '2img_tools').querySelector('.form')

		button.removeAttribute('id')
		button.removeAttribute('title')
		button.classList.add('tool')

		button.addEventListener('click', () => {
			if (extraNetwork.classList.contains('secondary-down'))
				extraNetwork.dispatchEvent(new Event('click'))

			this.isOns[index] = !this.isOns[index]
			this.ez_containers[index].style.display = this.isOns[index] ? 'block' : 'none'
		})

		extraNetwork.addEventListener('click', () => {
			if (this.ez_containers[index].style.display != 'none')
				button.dispatchEvent(new Event('click'))
		})

		const applyStyle = actionColumn.children[3]
		actionColumn.insertBefore(button, applyStyle)
	}

	main() {
		for (let i = injectUtil.TXT2IMG; i <= injectUtil.IMG2IMG; i++) {

			this.toprows[i].after(this.ez_containers[i])

			this.ez_containers[i].style.borderStyle = 'none'
			this.ez_containers[i].style.display = 'none'

			this.refresh_btns[i].addEventListener('click', () => {
				setTimeout(this.pollCollection, 250)
			})

			this.to_negatives[i].classList.remove('block')

			this.to_negatives[i].style.margin = '0.3em'
			this.to_negatives[i].style.marginLeft = '4'
			this.to_negatives[i].style.marginRight = 0

			this.refresh_btns[i].style.margin = '0.3em'
			this.refresh_btns[i].style.marginLeft = 'auto'
			this.refresh_btns[i].style.marginRight = 0


			this.tabs[i].appendChild(this.refresh_btns[i])
			this.tabs[i].appendChild(this.to_negatives[i])

			this.tabRows[i].forEach((tab) => {
				let buttons = tab.querySelectorAll("button")

				buttons.forEach((button) => {
					if (!button.id.includes('ez-tag'))
						this.injectButton(button, i)
				})
			})

			this.openButton(i)
		}
	}
}

onUiLoaded(async () => {
	const injector = new le_Injector()
	injector.main()
})