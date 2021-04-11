class Sheet {
    constructor(div) {
        this.container = div;
        this.items = [];
        this.separators = [];
        this.itemIdsToDelete = [];
    }

    loadItems(dataIdentifier) {
        var items = JSON.parse(document.getElementById(dataIdentifier).textContent);
        for (var index in items) {
            this.displayItem(items[index]);
        }
    }

    displayItem(data = {}) {
        if (this.items.length != 0) {
            // This is not the first item; display the seperator above.
            var seperatorAbove = document.createElement('hr');
            this.separators.push(seperatorAbove)
            this.container.appendChild(seperatorAbove);
        }

        var sheetItem = new SheetItem(this, data);
        this.items.push(sheetItem);
        this.container.appendChild(sheetItem.getContainer());
    }

    removeItem(item) {
        var itemIndex = this.items.indexOf(item);

        if (this.separators.length) {
            // Delete and remove seperator
            this.separators.splice(Math.max(0, itemIndex - 1), 1)[0].remove();
        }

        // Delete and remove item
        this.items.splice(itemIndex, 1);
        item.container.remove();

        if (item.id != -1) {
            // Item exists in database. Mark for deletion.
            this.itemIdsToDelete.push(item.id);
        }
    }

    submit() {
        var itemIdsToDeleteInput = document.createElement('input');
        itemIdsToDeleteInput.type = 'hidden';
        itemIdsToDeleteInput.name = 'itemIdsToDelete';
        itemIdsToDeleteInput.value = this.itemIdsToDelete.join('|');
        this.container.appendChild(itemIdsToDeleteInput);

        document.getElementById('pageForm').submit();
    }
}

class SheetItem {
    constructor(sheet, data) {
        this.sheet = sheet;
        this.id = Object.keys(data).length ? data['id'] : -1;

        var container = document.createElement('div');
        container.className = 'item';
        this.container = container;

        this.baseFields = [new TextInputField(data['title']), new TextAreaField(data['description'])];
        this.fieldOptions = [new PriceField(true, data['price']), new LocationField(true, data['location']), new DatetimeField(true, data['startDatetime'], data['endDatetime'], data['repeating'])];

        this.buildContainer();
    }

    parent() {
        return this.sheet;
    }

    buildContainer() {
        var idInput = document.createElement('input');
        idInput.type = 'hidden';
        idInput.name = 'id';
        idInput.value = this.id;
        this.container.appendChild(idInput);

        // Always display base fields
        for (var index in this.baseFields) {
            this.container.appendChild(this.baseFields[index].getContainer());
        }

        var actionsContainer = document.createElement('div');
        actionsContainer.className = 'actions';

        var fieldOptionsContainer = document.createElement('div');
        fieldOptionsContainer.className = 'field-options';

        for (var index in this.fieldOptions) {
            var field = this.fieldOptions[index];

            // Update the field's container/button visibility based on existing values
            field.updateVisibility(field.hasPrimaryValues() || field.hasSecondaryValues());
            this.container.appendChild(field.getContainer());
            fieldOptionsContainer.appendChild(field.getButton());
        }

        actionsContainer.appendChild(fieldOptionsContainer);

        var removeButton = document.createElement('button');
        removeButton.type = 'button';
        var thiss = this;
        removeButton.onclick = function () {
            thiss.parent().removeItem(thiss);
        }
        removeButton.textContent = 'Remove';

        actionsContainer.appendChild(removeButton);

        this.container.appendChild(actionsContainer);
    }

    getContainer() {
        return this.container;
    }
}
