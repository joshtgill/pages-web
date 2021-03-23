class Sheet {
    constructor(div) {
        this.container = div;
        this.items = [];
        this.separators = [];
    }

    loadItems(dataIdentifier) {
        var items = JSON.parse(document.getElementById(dataIdentifier).textContent);
        for (var index in items) {
            this.displayItem(items[index]);
        }
    }

    displayItem(data = null) {
        if (this.items.length != 0) {
            // Not displaying the first item, so display the seperator above.
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

        // Delete and remove seperator
        this.separators.splice(Math.max(0, itemIndex - 1), 1)[0].remove();

        // Delete and remove item
        this.items.splice(itemIndex, 1);
        item.container.remove();
    }
}

sheet = new Sheet(document.getElementById('items'));


class SheetItem {
    constructor(sheet, data) {
        this.sheet = sheet;

        var container = document.createElement('div');
        container.className = 'item';
        this.container = container;

        if (data) {
            // Initialize with existing data
            this.baseFields = [new TextInputField(data['title']), new TextAreaField(data['description'])];
            this.fieldOptions = [new PriceField(this, true, data['price']), new DatetimeField(this, false)];
        }
        else {
            this.baseFields = [new TextInputField(), new TextAreaField()];
            this.fieldOptions = [new PriceField(this, true), new DatetimeField(this, false)];
        }

        this.buildContainer();
    }

    parent() {
        return this.sheet;
    }

    buildContainer() {
        for (var index in this.baseFields) {
            this.container.appendChild(this.baseFields[index].getContainer());
        }

        var actionsContainer = document.createElement('div');
        actionsContainer.className = 'actions';

        var fieldOptionsContainer = document.createElement('div');
        this.fieldOptionsContainer = fieldOptionsContainer;
        fieldOptionsContainer.className = 'field-options';
        for (var index in this.fieldOptions) {
            var field = this.fieldOptions[index];
            field.hasValue() ? this.displayField(field) : this.displayFieldButton(field);
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

    displayField(field) {
        if (!field.isFirst && this.container.childElementCount == 4) {
            this.container.insertBefore(field.getContainer(), this.container.children[3]);
        }
        else {
            this.container.insertBefore(field.getContainer(), this.container.children[2]);
        }

        field.button.remove();
    }

    removeField(field) {
        field.container.remove();
        this.displayFieldButton(field);
    }

    displayFieldButton(field) {
        if (field.isFirst && this.container.childElementCount != 0) {
            this.fieldOptionsContainer.insertBefore(field.getButton(), this.fieldOptionsContainer.children[0]);
        }
        else {
            this.fieldOptionsContainer.appendChild(field.getButton());
        }
    }
}

class BaseField {
    constructor(container, value) {
        this.container = container;

        this.valueProvided = value != null;
        this.buildContainer(value);
    }

    hasValue() {
        return this.valueProvided;
    }

    buildContainer() {
        console.log('BaseField::buildContainer(): Unhandled');
    }

    getContainer() {
        return this.container;
    }
}

class BaseOptionalField extends BaseField {
    constructor(sheetItem, isFirst, button, container, value) {
        super(container, value);
        this.sheetItem = sheetItem;
        this.isFirst = isFirst;
        this.button = button;

        this.buildButton();
    }

    parent() {
        return this.sheetItem;
    }

    buildButton() {
        console.log('BaseOptionalField::buildButton(): Unhandled');
    }

    getButton() {
        return this.button;
    }

    buildRemoveFieldButton() {
        var removeFieldButton = document.createElement('button');
        removeFieldButton.type = 'button';
        var thiss = this;
        removeFieldButton.onclick = function () {
            thiss.parent().removeField(thiss);
        }

        var removeFieldIcon = document.createElement('img');
        removeFieldIcon.src = '/static/images/clear.png';
        removeFieldIcon.alt = 'remove';

        removeFieldButton.appendChild(removeFieldIcon);

        return removeFieldButton;
    }
}

class TextInputField extends BaseField {
    constructor(value) {
        super(document.createElement('input'), value);
    }

    buildContainer(value) {
        this.container.id = 'sheetItemTitle';
        this.container.name = 'title';
        this.container.type = 'text';
        this.container.placeholder = 'Title';
        this.container.autocomplete = 'off';
        if (value) {
            this.container.value = value;
        }
    }
}

class TextAreaField extends BaseField {
    constructor(value) {
        super(document.createElement('textarea'), value);
    }

    buildContainer(value) {
        this.container.name = 'description';
        this.container.rows = 3;
        this.container.placeholder = 'Description';
        if (value) {
            this.container.value = value;
        }
    }
}

class PriceField extends BaseOptionalField {
    constructor(sheetItem, isFirst, value) {
        super(sheetItem, isFirst, document.createElement('button'), document.createElement('div'), value);
    }

    buildButton() {
        this.button.id = 'priceButton';
        this.button.type = 'button';
        var thiss = this;
        this.button.onclick = function () {
            thiss.parent().displayField(thiss);
        }
        this.button.textContent = '$';
    }

    buildContainer(value) {
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
        if (value) {
            priceInput.value = value;
        }
        this.container.appendChild(priceInput);

        this.container.appendChild(super.buildRemoveFieldButton(this.container));
    }
}

class DatetimeField extends BaseOptionalField {
    constructor(sheetItem, isFirst) {
        super(sheetItem, isFirst, document.createElement('button'), document.createElement('div'));
    }

    buildButton() {
        this.button.type = 'button';
        var thiss = this;
        this.button.onclick = function () {
            thiss.parent().displayField(thiss);
        }

        var datetimeFieldIcon = document.createElement('img');
        datetimeFieldIcon.src = '/static/images/clock.png';
        datetimeFieldIcon.alt = 'clock';

        this.button.appendChild(datetimeFieldIcon);
    }

    buildContainer() {
        this.container.className = 'datetime-container';

        var startInput = document.createElement('input');
        startInput.type = 'datetime-local';
        this.container.appendChild(startInput);

        var toWord = document.createElement('h3');
        toWord.textContent = 'to';
        this.container.appendChild(toWord)

        var endInput = document.createElement('input');
        endInput.type = 'datetime-local';
        this.container.appendChild(endInput);

        this.container.appendChild(super.buildRemoveFieldButton(this.container));
    }
}

function removeAndRecordPageItemForDeletion(pageItemId, sourceButton) {
    removePageItem(sourceButton);

    // Record Page ID to be deleted on Page save
    var pageItemIdsToDelete = document.getElementById('pageItemIdsToDelete');
    pageItemIdsToDelete.value += !pageItemIdsToDelete.value ? pageItemId
        : pageItemIdsToDelete.value += `|${pageItemId}`;
}

function removePageItem(sourceButton) {
    // Remove Page item from page
    // TODO: Removing the first Page item causes an unwanted <hr>
    sourceButton.parentNode.parentNode.remove();
}

function submitPageDeleteForm() {
    document.getElementById('pageDeleteForm').submit();
}
