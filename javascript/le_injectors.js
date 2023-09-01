class le_Injector {

	constructor() {
		this.toprows = injectUtils.getToprows()
		this.containers = injectUtils.getContainers()
		this.tabNavs = injectUtils.getTabNavs(this.containers)
		this.refresh_btns = injectUtils.getRefreshs()
		this.to_negatives = injectUtils.getToNegs()
		this.tabRows = injectUtils.getTabRows(this.containers)
		this.isOns = [false, false]
		this.cachedDict = null
		this.dummy = document.getElementById('ez-tag-textbox').querySelector('textarea')

		this.extraBtnCount = 1
	}

	injectButton(button, index) {
		const mode = injectUtils.Modes[index]

		button.addEventListener('click', () => {
			const checkbox = this.to_negatives[index].querySelector('input[type=checkbox]')
			const id = mode + (checkbox.checked ? '2img_neg_prompt' : '2img_prompt')
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

	pollCollection = (tryIteration) => {
		// First Refresh
		if (!this.cachedDict) {
			if (this.dummy.value.length < 1) {
				setTimeout(() => { this.pollCollection(69) }, 25)
				return;
			}
		}	// Subsequent Refresh
		else {
			if (tryIteration > 5) {
				console.log("[EasyTagInsert]: Refresh Timeout!")
				return;
			}
			if (this.dummy.value == this.cachedDict) {
				setTimeout(() => { this.pollCollection(tryIteration + 1) }, 100)
				return;
			}
		}

		this.cachedDict = this.dummy.value
		const dictionary = JSON.parse(this.dummy.value.replace(/'/g, '"').replace(/None/g, '""'))
		this.reconstructUI(dictionary)
	}

	reconstructUI(dictionary) {
		if (Object.keys(dictionary).length !== this.tabNavs[injectUtils.TXT2IMG].getElementsByTagName('button').length - this.extraBtnCount) {
			alert('Modifying Categories is not Supported yet!')
			return;
		}

		for (let index = injectUtils.TXT2IMG; index <= injectUtils.IMG2IMG; index++) {
			const mode = injectUtils.Modes[index]

			for (let key in dictionary) {
				const section = document.getElementById('tab-' + key.replace(/ /g, '-').toLowerCase() + '-' + mode)
				let buttons = section.getElementsByTagName('button')

				const btnKeys = Array.from(buttons).map(button => button.innerText)
				const dictKeys = Object.keys(dictionary[key]).filter(k => dictionary[key][k] != "")

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
		const mode = injectUtils.Modes[index]

		const button = document.getElementById('ez-tag-toggle-' + mode)
		const actionColumn = document.getElementById(mode + '2img_tools').querySelector('.form')

		button.removeAttribute('id')
		button.removeAttribute('title')
		button.classList.add('tool')

		button.addEventListener('click', () => {
			this.isOns[index] = !this.isOns[index]
			this.containers[index].style.display = this.isOns[index] ? 'block' : 'none'
		})

		actionColumn.append(button)
	}

	main() {
		for (let i = injectUtils.TXT2IMG; i <= injectUtils.IMG2IMG; i++) {

			this.toprows[i].after(this.containers[i])

			this.containers[i].style.borderStyle = 'none'
			this.containers[i].style.display = 'none'

			this.refresh_btns[i].addEventListener('click', () => { this.pollCollection(0) })

			this.to_negatives[i].classList.remove('block')

			this.to_negatives[i].style.margin = '0.3em'
			this.to_negatives[i].style.marginLeft = '4'
			this.to_negatives[i].style.marginRight = 0

			this.refresh_btns[i].style.margin = '0.3em'
			this.refresh_btns[i].style.marginLeft = 'auto'
			this.refresh_btns[i].style.marginRight = 0


			this.tabNavs[i].appendChild(this.refresh_btns[i])
			this.tabNavs[i].appendChild(this.to_negatives[i])

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