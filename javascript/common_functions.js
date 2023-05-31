function pollCollection() {
	const dummy = document.getElementById('ez-tag-textbox').querySelector('textarea')
	if (dummy.value.length < 1) { setTimeout(pollCollection, 100); }

	else {
		const dictionary = JSON.parse(dummy.value.replace(/'/g, '"'));

		LeInjector_TXT.reconstructUI(dictionary)
		LeInjector_IMG.reconstructUI(dictionary)
	}
}

function checkTabCount(dicLen, tabLen) {
	if (dicLen !== tabLen) console.log('Modifying Tabs is currently not supported. Please Reload UI!')
	return dicLen !== tabLen
}