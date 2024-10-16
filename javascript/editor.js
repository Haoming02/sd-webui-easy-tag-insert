class EasyTagEditor {

    static #headers = ["Category", "Name", "Prompt", "Del"];
    static #columnWidth = ["15%", "15%", "65%", "5%"];

    /** @type {HTMLTableElement} */
    static #table = undefined;
    /** @type {HTMLTextAreaElement} */
    static #field = undefined;
    /** @type {HTMLButtonElement} */
    static #button = undefined;

    /** @param {HTMLDivElement} frame */
    static #constructTable(frame) {
        const table = document.createElement("table");

        const colgroup = document.createElement('colgroup');
        for (let c = 0; c < this.#headers.length; c++) {
            const col = document.createElement('col');
            col.style.width = this.#columnWidth[c];
            colgroup.appendChild(col);
        }
        table.appendChild(colgroup);

        const thead = document.createElement('thead');
        const thr = thead.insertRow();
        for (let c = 0; c < this.#headers.length; c++) {
            const th = document.createElement('th');
            th.textContent = this.#headers[c];
            thr.appendChild(th);
        }
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        table.appendChild(tbody);
        this.#table = tbody;

        frame.appendChild(table);
    }

    static init() {
        this.#field = document.getElementById("ez-editor-box").querySelector("textarea");
        this.#button = document.getElementById("ez-editor-btn");
        this.#constructTable(document.getElementById("ez-editor"));

        this.#table.addEventListener("keyup", () => { this.#onEdit(); });
        this.#table.addEventListener("paste", (e) => {
            e.preventDefault();
            const text = e.clipboardData.getData('text/plain');
            const selection = window.getSelection();

            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                range.deleteContents();
                const node = document.createTextNode(text);
                range.insertNode(node);

                range.setStartAfter(node);
                range.collapse(true);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        });
    }

    static save() {
        const DATA = {};
        const rows = this.#table.querySelectorAll("tr");

        rows.forEach((row) => {
            const cells = row.querySelectorAll("td");
            const category = cells[0].textContent.trim();
            const name = cells[1].textContent.trim();
            const prompt = cells[2].textContent.trim();

            if ((!category) || (!name) || (!prompt))
                return;

            if (!(category in DATA))
                DATA[category] = { [name]: prompt };
            else
                DATA[category][name] = prompt;
        });

        this.#field.value = JSON.stringify(DATA);
        updateInput(this.#field);
        this.#button.click();
    }

    static load() {
        while (this.#table.firstChild)
            this.#table.removeChild(this.#table.firstChild);

        const val = this.#field.value;
        if (!val.trim()) {
            this.#addRow(["", "", ""]);
            return;
        }

        const data = JSON.parse(val);
        for (const [category, cards] of Object.entries(data)) {
            for (const [name, prompt] of Object.entries(cards)) {
                this.#addRow([category, name, prompt])
            }
        }

        this.#addRow(["", "", ""]);
    }

    /** @param {string[]} content [category, name, prompt] */
    static #addRow(content) {
        const tr = this.#table.insertRow();
        for (let c = 0; c < this.#headers.length - 1; c++) {
            const td = tr.insertCell();
            td.contentEditable = true;
            td.textContent = content[c];
        }

        const td = tr.insertCell();
        td.style.textAlign = "center";
        const del = document.createElement("button");
        del.title = "Delete this Card";
        del.style.margin = "auto";
        del.textContent = "❌";
        td.appendChild(del);

        del.onclick = () => { tr.remove(); this.#onEdit(); }
    }

    static #onEdit() {
        const rows = this.#table.querySelectorAll("tr");
        const count = rows.length;

        for (let i = count - 1; i >= 0; i--)
            if (this.#isEmpty(rows[i]))
                rows[i].remove();

        this.#addRow(["", "", ""]);
    }

    /** @param {HTMLTableRowElement} row  @returns {boolean} */
    static #isEmpty(row) {
        const cells = row.querySelectorAll("td");
        return (
            (!cells[0].textContent.trim()) &&
            (!cells[1].textContent.trim()) &&
            (!cells[2].textContent.trim())
        )
    }

}

onUiLoaded(() => {
    EasyTagEditor.init();
    ['txt', 'img'].forEach((mode) => {
        const container = document.getElementById(`${mode}2img_ez_tags_cards_html`);
        container.classList.add("ez-tag-container");
    });
});
