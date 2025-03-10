class EasyTagEditor {

    /** @type {HTMLTableElement} */
    static #table;
    /** @type {HTMLTextAreaElement} */
    static #field;
    /** @type {HTMLButtonElement} */
    static #button;

    /** @param {HTMLDivElement} frame */
    static #constructTable(frame) {
        const table = document.createElement("table");
        const thead = document.createElement('thead');

        const columnWidths = ["15%", "15%", "65%", "5%"];
        const colgroup = document.createElement('colgroup');
        for (const width of columnWidths) {
            const col = document.createElement('col');
            col.style.width = width;
            colgroup.appendChild(col);
        }
        table.appendChild(colgroup);

        const headers = ["Category", "Name", "Prompt", "Del"];
        const thr = thead.insertRow();
        for (const header of headers) {
            const th = document.createElement('th');
            th.textContent = header;
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
        const data = {};
        const rows = this.#table.querySelectorAll("tr");

        for (const row of rows) {
            const cells = row.querySelectorAll("td");
            const category = cells[0].textContent.trim();
            const name = cells[1].textContent.trim();
            const prompt = cells[2].textContent.trim();

            if ((!category) || (!name) || (!prompt))
                continue;

            if (!data.hasOwnProperty(category))
                data[category] = {};

            data[category][name] = prompt;
        }

        this.#field.value = JSON.stringify(data);
        updateInput(this.#field);
        this.#button.click();
    }

    static load() {
        while (this.#table.firstChild)
            this.#table.removeChild(this.#table.firstChild);

        const val = this.#field.value;
        if (Boolean(val.trim())) {
            const data = JSON.parse(val);
            for (const [category, cards] of Object.entries(data)) {
                for (const [name, prompt] of Object.entries(cards))
                    this.#addRow([category, name, prompt])
            }
        }

        this.#addRow(["", "", ""]);
    }

    /** @param {string[]} content [category, name, prompt] */
    static #addRow(content) {
        const tr = this.#table.insertRow();

        for (const txt of content) {
            const td = tr.insertCell();
            td.contentEditable = true;
            td.textContent = txt;
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

    /** @param {HTMLTableRowElement} row @returns {boolean} */
    static #isEmpty(row) {
        const cells = row.querySelectorAll("td");
        return (
            (!cells[0].textContent.trim()) &&
            (!cells[1].textContent.trim()) &&
            (!cells[2].textContent.trim())
        )
    }

}

onUiLoaded(() => { EasyTagEditor.init(); });
