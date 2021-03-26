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
        this.fieldOptions = [new PriceField(data['price']), new LocationField(data['location']), new DatetimeField(data['startDatetime'], data['endDatetime'])];

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
        return this.values[0] != null && this.values[0] != '';
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
        super(document.createElement('div'), args);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'title-field-container';

        var titleInput = document.createElement('input');
        titleInput.name = 'title';
        titleInput.type = 'text';
        titleInput.placeholder = 'Title';
        titleInput.autocomplete = 'off';
        titleInput.value = this.hasValues() ? this.values[0] : '';

        this.container.appendChild(titleInput);
    }
}

class TextAreaField extends BaseField {
    constructor(...args) {
        super(document.createElement('div'), args);
    }

    buildContainer() {
        this.container.className = 'field-container';

        var descriptionTextArea = document.createElement('textarea');
        descriptionTextArea.name = 'description';
        descriptionTextArea.rows = 3;
        descriptionTextArea.placeholder = 'Description';
        descriptionTextArea.value = this.hasValues() ? this.values[0] : '';

        this.container.appendChild(descriptionTextArea);
    }
}

class PriceField extends BaseOptionalField {
    constructor(...args) {
        super(document.createElement('button'), document.createElement('div'), args);
    }

    buildButton() {
        super.buildButton();

        var priceFieldIcon = document.createElement('img');
        priceFieldIcon.src = '/static/images/price.png';
        priceFieldIcon.alt = 'price';

        this.button.appendChild(priceFieldIcon);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'price-field-container';

        var priceIcon = document.createElement('img');
        priceIcon.src = '/static/images/price.png';
        priceIcon.alt = 'price';
        this.container.appendChild(priceIcon);

        var priceInput = document.createElement('input');
        priceInput.id = 'sheetItemPrice';
        priceInput.name = 'price';
        priceInput.type = 'number';
        priceInput.step = '0.01';
        priceInput.placeholder = 'Price';
        priceInput.value = this.hasValues() ? this.values[0] : '';
        this.container.appendChild(priceInput);

        this.container.appendChild(super.buildRemoveFieldButton());
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
        datetimeFieldIcon.src = '/static/images/datetime.png';
        datetimeFieldIcon.alt = 'clock';

        this.button.appendChild(datetimeFieldIcon);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'datetime-field-container';

        var datetimeFieldIcon = document.createElement('img');
        datetimeFieldIcon.src = '/static/images/datetime.png';
        datetimeFieldIcon.alt = 'clock';
        this.container.appendChild(datetimeFieldIcon);

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

        this.container.appendChild(super.buildRemoveFieldButton());
    }

    hasValues() {
        return this.values[0] != null || this.values[1] != null;
    }

    nullValues() {
        this.container.querySelector('input[name="startDatetime"]').value = '';
        this.container.querySelector('input[name="endDatetime"]').value = '';
    }
}

class LocationField extends BaseOptionalField {
    constructor(...args) {
        super(document.createElement('button'), document.createElement('div'), args);
    }

    buildButton() {
        super.buildButton();

        var locationFieldIcon = document.createElement('img');
        locationFieldIcon.src = '/static/images/location.png';
        locationFieldIcon.alt = 'location';

        this.button.appendChild(locationFieldIcon);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'location-field-container';

        var locationIcon = document.createElement('img');
        locationIcon.src = '/static/images/location.png';
        locationIcon.alt = 'price';
        this.container.appendChild(locationIcon);

        var locationInput = document.createElement('input');
        locationInput.name = 'location';
        locationInput.type = 'text';
        locationInput.placeholder = 'Location';
        locationInput.autocomplete = 'off';
        locationInput.value = this.hasValues() ? this.values[0] : '';
        this.container.appendChild(locationInput);

        this.container.appendChild(super.buildRemoveFieldButton());
    }

    nullValues() {
        this.container.querySelector('input[name="location"]').value = '';
    }
}

sheet = new Sheet(document.getElementById('items'));
