class Page {
    constructor(Item, dataIdentifier=null) {
        this.Item = Item;
        this.container = document.getElementById('items');
        this.items = [];
        this.separators = [];

        // Need to track existing items that are deleted
        var itemIdsToDeleteInput = document.createElement('input');
        this.itemIdsToDeleteInput = itemIdsToDeleteInput;
        itemIdsToDeleteInput.type = 'hidden';
        itemIdsToDeleteInput.name = 'itemIdsToDelete';
        this.container.appendChild(this.itemIdsToDeleteInput);

        if (dataIdentifier) {
            var itemsData = JSON.parse(document.getElementById(dataIdentifier).textContent);
            for (var index in itemsData) {
                this.addItem(itemsData[index]);
            }
        }
    }

    addItem(data = {}) {
        if (this.items.length != 0) {
            // This is not the first item, display the separator above.
            var seperatorAbove = document.createElement('hr');
            this.separators.push(seperatorAbove)
            this.container.appendChild(seperatorAbove);
        }

        var item = new this.Item(this, data);
        this.items.push(item);
        this.container.appendChild(item.getContainer());
    }

    removeItem(item) {
        var itemIndex = this.items.indexOf(item);

        if (this.separators.length) {
            // Delete and remove separator
            this.separators.splice(Math.max(0, itemIndex - 1), 1)[0].remove();
        }

        // Delete and remove item
        this.items.splice(itemIndex, 1);
        item.container.remove();

        if (item.id != -1) {
            // Item exists in database. Mark for deletion.
            var itemIdsToDelete = this.itemIdsToDeleteInput.value == '' ? [] : this.itemIdsToDeleteInput.value.split('|');
            itemIdsToDelete.push(item.id);
            this.itemIdsToDeleteInput.value = itemIdsToDelete.join('|');
        }
    }
}


class SheetItem {
    constructor(page, data) {
        this.page = page;

        this.id = Object.keys(data).length ? data['id'] : -1;
        this.fields = [new TextInputField('title', 'Title', data['title']),
                       new TextAreaField(data['description']),
                       new PriceField(true, data['price']),
                       new LocationField(true, data['location']),
                       new DatetimeField(true, data['singleOccurence'], data['repeatingOccurence'])];

        this.container = null;
        this.buildContainer();
    }

    parent() {
        return this.page;
    }

    buildContainer() {
        this.container = document.createElement('div');
        this.container.className = 'item';
        this.container.innerHTML = `
            <input type="hidden" name="id" value="${this.id}">

            <div class="actions">
                <div class="field-options">
                </div>
                <button type="button" id="removeButton">Remove</button>
            </div>
        `;

        this.detailContainer();
    }

    detailContainer() {
        for (var i = this.fields.length - 1; i >= 0; --i) {
            var field = this.fields[i];

            this.container.insertBefore(field.getContainer(), this.container.children[0]);
            if (field.isOptional) {
                field.toggle(field.hasPrimaryValues() || field.hasSecondaryValues());
                this.container.querySelector('.field-options').insertBefore(field.getButton(),
                                                                            this.container.querySelector('.field-options').children[0]);
            }
        }

        var thiss = this;
        this.container.querySelector('#removeButton').onclick = function() {
            thiss.parent().removeItem(thiss);
        }
    }

    getContainer() {
        return this.container;
    }
}


class ChecklistItem {
    constructor(page, data) {
        this.page = page;

        this.id = Object.keys(data).length ? data['id'] : -1;
        this.fields = [new TextInputField('text', 'Item text', data['text']),
                       new TextAreaField(true, data['description'])];

        this.container = null;
        this.buildContainer();
    }

    parent() {
        return this.page;
    }

    buildContainer() {
        this.container = document.createElement('div');
        this.container.className = 'item';
        this.container.innerHTML = `
            <input type="hidden" name="id" value="${this.id}">

            <div class="actions">
                <div class="field-options">
                </div>
                <button type="button" id="removeButton">Remove</button>
            </div>
        `;

        this.detailContainer();
    }

    detailContainer() {
        for (var i = this.fields.length - 1; i >= 0; --i) {
            var field = this.fields[i];

            this.container.insertBefore(field.getContainer(), this.container.children[0]);
            if (field.isOptional) {
                field.toggle(field.hasPrimaryValues() || field.hasSecondaryValues());
                this.container.querySelector('.field-options').insertBefore(field.getButton(),
                                                                            this.container.querySelector('.field-options').children[0]);
            }
        }

        var thiss = this;
        this.container.querySelector('#removeButton').onclick = function() {
            thiss.parent().removeItem(thiss);
        }
    }

    getContainer() {
        return this.container;
    }
}


class EventItem {
    constructor(page, data) {
        this.page = page;

        this.id = Object.keys(data).length ? data['id'] : -1;
        this.fields = [new TextAreaField(false, data['description']),
                       new LocationField(false, data['location']),
                       new DatetimeField(false, data['singleOccurence'], data['repeatingOccurence']),
                       new ToggleField(data['attendanceIsPublic'])];

        this.container = null;
        this.buildContainer();
    }

    parent() {
        return this.page;
    }

    buildContainer() {
        this.container = document.createElement('div');
        this.container.className = 'item';
        this.container.innerHTML = `
            <input type="hidden" name="id" value="${this.id}">

            <div class="actions">
                <div class="field-options">
                </div>
                <button type="button" id="removeButton">Remove</button>
            </div>
        `;

        this.detailContainer();
    }

    detailContainer() {
        for (var i = this.fields.length - 1; i >= 0; --i) {
            var field = this.fields[i];

            this.container.insertBefore(field.getContainer(), this.container.children[0]);
            if (field.isOptional) {
                field.toggle(field.hasPrimaryValues() || field.hasSecondaryValues());
                this.container.querySelector('.field-options').insertBefore(field.getButton(),
                                                                            this.container.querySelector('.field-options').children[0]);
            }
        }

        var thiss = this;
        this.container.querySelector('#removeButton').onclick = function() {
            thiss.parent().removeItem(thiss);
        }
    }

    getContainer() {
        return this.container;
    }
}
