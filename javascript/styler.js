class EasyTagStyler {

    static init() {
        ["txt", "img"].forEach((mode) => {
            const btn = document.getElementById(`${mode}2img_ez_tags_extra_refresh`);
            btn.addEventListener("click", () => {
                setTimeout(() => this.#addStyle(mode), 100);
            });
        });

        setTimeout(() => this.#addStyle("txt"), 100);
    }

    /** @param {string} mode "txt" | "img" */
    static #addStyle(mode) {
        const page = document.getElementById(`${mode}2img_ez_tags_cards_html`);
        if (page.querySelector(".pending") != null) {
            setTimeout(() => this.#addStyle(mode), 100);
            return;
        }

        if (page.querySelector(".style-bracket") != null)
            return;

        [
            document.getElementById("txt2img_ez_tags_cards"),
            document.getElementById("img2img_ez_tags_cards")
        ].forEach((cardList) => {
            const cards = cardList.querySelectorAll("div.card");
            if (cards.length === 0) {
                const empty = document.createElement("div");
                empty.classList.add("style-bracket");
                page.appendChild(empty);
                return;
            }

            const categories = {};
            cards.forEach((card) => {
                const data = card.getAttribute("data-sort-date_modified");
                const key = data.substring(0, data.length - 3);

                if (categories.hasOwnProperty(key))
                    categories[key].push(card);
                else
                    categories[key] = [card];
            });

            for (const [key, value] of Object.entries(categories)) {
                const category = document.createElement("div");
                category.classList.add("style-bracket");
                category.setAttribute("category", key);

                const label = document.createElement("span");
                label.textContent = key.replaceAll("_", " ");
                const container = document.createElement("div");
                value.forEach((card) => { container.appendChild(card); });

                category.appendChild(label);
                category.appendChild(container);
                cardList.appendChild(category);
            }
        })
    }

}
