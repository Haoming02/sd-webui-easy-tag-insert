class EasyTagStyler {

    static #refresh = { "txt": null, "img": null };

    static init() {
        for (const mode of ["txt", "img"]) {
            const observer = new MutationObserver((mutationsList) => {
                for (const mutation of mutationsList) {
                    if (mutation.type === "childList") {
                        const timer = this.#refresh[mode];
                        if (timer) clearTimeout(timer);

                        this.#refresh[mode] = setTimeout(() => { this.#addStyle(mode); }, 250);
                        return;
                    }
                }
            });

            const page = document.getElementById(`${mode}2img_ez-tags_cards_html`);
            observer.observe(page, { childList: true, subtree: true });
        }
    }

    /** @param {string} mode "txt" | "img" */
    static #addStyle(mode) {
        const page = document.getElementById(`${mode}2img_ez-tags_cards_html`);
        if (page.querySelector(".pending") != null)
            setTimeout(() => this.#addStyle(mode), 100);
        if (page.querySelector(".style-bracket") != null)
            return;

        const cardList = document.getElementById(`${mode}2img_ez-tags_cards`);
        const cards = cardList.querySelectorAll("div.card");
        if (cards.length === 0)
            return;

        const categories = {};
        for (const card of cards) {
            const data = card.getAttribute("data-sort-date_modified");
            const key = data.substring(0, data.length - 3);

            if (categories.hasOwnProperty(key))
                categories[key].push(card);
            else
                categories[key] = [card];
        }

        for (const [key, value] of Object.entries(categories)) {
            const category = document.createElement("div");
            category.classList.add("style-bracket");
            category.setAttribute("category", key);

            const label = document.createElement("span");
            label.textContent = key.replaceAll("-", " ");
            label.setAttribute("align", "center");
            const container = document.createElement("div");
            value.forEach((card) => { container.appendChild(card); });

            category.appendChild(label);
            category.appendChild(container);
            cardList.appendChild(category);
        }
    }

}

onUiLoaded(() => {
    const config = document.getElementById("setting_ez_use_category").querySelector("input[type=checkbox]");
    if (!config.checked)
        return;

    for (const mode of ['txt', 'img']) {
        const container = document.getElementById(`${mode}2img_ez-tags_cards_html`);
        container.classList.add("ez-tag-container");
    }

    EasyTagStyler.init();
});
