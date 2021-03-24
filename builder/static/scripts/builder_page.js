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
        itemIdsToDeleteInput.className = 'hidden';
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
        this.fieldOptions = [new PriceField(data['price']), new DatetimeField(data['startDatetime'], data['endDatetime'])];

        this.buildContainer();
    }

    parent() {
        return this.sheet;
    }

    buildContainer() {
        var idInput = document.createElement('input');
        idInput.className = 'hidden';
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
            field.updateVisibility(field.hasValues());
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

class BaseField {
    constructor(container, values) {
        this.container = container;
        this.values = values;

        this.buildContainer();
    }

    buildContainer() {
        console.log('BaseField::buildContainer(): Unhandled');
    }

    getContainer() {
        return this.container;
    }

    hasValues() {
        return this.values[0] != null;
    }
}

class BaseOptionalField extends BaseField {
    constructor(button, container, values) {
        super(container, values);
        this.button = button;

        this.buildButton();
    }

    buildButton() {
        this.button.type = 'button';
        var thiss = this;
        this.button.onclick = function () {
            thiss.updateVisibility(true);
        }
    }

    getButton() {
        return this.button;
    }

    buildRemoveFieldButton() {
        var removeFieldButton = document.createElement('button');
        removeFieldButton.type = 'button';
        var thiss = this;
        removeFieldButton.onclick = function () {
            thiss.updateVisibility(false);
        }

        var removeFieldIcon = document.createElement('img');
        removeFieldIcon.src = '/static/images/clear.png';
        removeFieldIcon.alt = 'remove';

        removeFieldButton.appendChild(removeFieldIcon);

        return removeFieldButton;
    }

    updateVisibility(container) {
        if (container) {
            this.container.style.display = 'flex';
            this.button.style.display = 'none';
        }
        else {
            this.button.style.display = 'inline-block';
            this.container.style.display = 'none';

            this.nullValues();
        }
    }

    nullValues() {
        console.log('BaseOptionalField::nullValues(): Unhandled');
    }
}

class TextInputField extends BaseField {
    constructor(...args) {
        super(document.createElement('input'), args);
    }

    buildContainer() {
        this.container.id = 'sheetItemTitle';
        this.container.name = 'title';
        this.container.type = 'text';
        this.container.placeholder = 'Title';
        this.container.autocomplete = 'off';
        this.container.value = this.hasValues() ? this.values[0] : '';
    }
}

class TextAreaField extends BaseField {
    constructor(...args) {
        super(document.createElement('textarea'), args);
    }

    buildContainer() {
        this.container.name = 'description';
        this.container.rows = 3;
        this.container.placeholder = 'Description';
        this.container.value = this.hasValues() ? this.values[0] : '';
    }
}

class PriceField extends BaseOptionalField {
    constructor(...args) {
        super(document.createElement('button'), document.createElement('div'), args);
    }

    buildButton() {
        super.buildButton();
        this.button.id = 'priceButton';
        this.button.textContent = '$';
    }

    buildContainer() {
        this.container.className = 'price-container';

        var moneySign = document.createElement('h3');
        moneySign.textContent = '$';
        this.container.appendChild(moneySign)

        var priceInput = document.createElement('input');
        priceInput.id = 'sheetItemPrice';
        priceInput.name = 'price';
        priceInput.type = 'number';
        priceInput.step = '0.01';
        priceInput.placeholder = 'Price';
        priceInput.value = this.hasValues() ? this.values[0] : '';

        this.container.appendChild(priceInput);

        this.container.appendChild(super.buildRemoveFieldButton(this.container));
    }

    nullValues() {
        this.container.querySelector('#sheetItemPrice').value = '';
    }
}

class DatetimeField extends BaseOptionalField {
    constructor(...args) {
        super(document.createElement('button'), document.createElement('div'), args);
    }

    buildButton() {
        super.buildButton();

        var datetimeFieldIcon = document.createElement('img');
        datetimeFieldIcon.src = '/static/images/clock.png';
        datetimeFieldIcon.alt = 'clock';

        this.button.appendChild(datetimeFieldIcon);
    }

    buildContainer() {
        this.container.className = 'datetime-container';

        var startInput = document.createElement('input');
        startInput.type = 'datetime-local';
        startInput.name = 'startDatetime';
        startInput.value = this.hasValues() ? this.values[0] : '';
        this.container.appendChild(startInput);

        var toWord = document.createElement('h3');
        toWord.textContent = 'to';
        this.container.appendChild(toWord)

        var endInput = document.createElement('input');
        endInput.type = 'datetime-local';
        endInput.name = 'endDatetime';
        endInput.value = this.hasValues() ? this.values[1] : '';
        this.container.appendChild(endInput);

        this.container.appendChild(super.buildRemoveFieldButton(this.container));
    }

    hasValues() {
        return this.values[0] != null || this.values[1] != null;
    }

    nullValues() {
        this.container.querySelector('input[name="startDatetime"]').value = '';
        this.container.querySelector('input[name="endDatetime"]').value = '';
    }
}

sheet = new Sheet(document.getElementById('items'));
