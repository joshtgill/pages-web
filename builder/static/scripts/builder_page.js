class Sheet
{
    constructor(div)
    {
        this.div = div;
    }

    displaySheetItems(dataIdentifier)
    {
        var sheetItems = JSON.parse(document.getElementById(dataIdentifier).textContent);
        for (var i = 0; i < sheetItems.length; i++)
        {
            var sheetItem = new SheetItem(this, sheetItems[i]);
            if (i < sheetItems.length - 1)
                this.div.appendChild(document.createElement('hr'));
        }
    }

    createEmptySheetItem()
    {
        if (this.div.childElementCount != 0)
            this.div.appendChild(document.createElement('hr'));

        var sheetItem = new SheetItem(this);
    }
}

sheet = new Sheet(document.getElementById('items'));


class SheetItem
{
    constructor(sheet, data=null)
    {
        this.sheet = sheet;
        this.textInputField = new TextInputField(this);
        this.textAreaField = new TextAreaField(this);
        this.priceField = new PriceField(this);
        this.datetimeField = new DatetimeField(this);

        var div = document.createElement('div');
        div.className = 'item';
        this.div = div;
        this.sheet.div.appendChild(this.div);

        this.displayFields(data);
        this.displayActions();
    }

    displayFields(data)
    {
        if (data)
        {
            this.textInputField.display(data['title']);
            this.textAreaField.display(data['description']);
            this.priceField.display(data['price']);
        }
        else
        {
            this.textInputField.display();
            this.textAreaField.display();
        }
    }

    displayActions()
    {
        var actions = document.createElement('div');
        actions.className = 'actions';

        var fieldOptions = document.createElement('div');
        fieldOptions.className = 'field-options';
        this.fieldOptions = fieldOptions; // Don't love

        this.priceField.displayButton();
        this.datetimeField.displayButton();
        actions.appendChild(fieldOptions);

        var removeButton = document.createElement('button');
        removeButton.type = 'button';
        var thiss = this;
        removeButton.onclick = function() { thiss.remove(); }
        removeButton.textContent = 'Remove item';

        actions.appendChild(removeButton);

        this.div.appendChild(actions);
    }

    remove()
    {
        this.div.remove();
    }

    priceFieldIsActive()
    {
        return this.div.querySelector('.price-container') != null;
    }
}

class BaseField
{
    buildRemoveFieldButton(fieldContainer)
    {
        var removeFieldButton = document.createElement('button');
        removeFieldButton.type = 'button';
        var thiss = this;
        removeFieldButton.onclick = function() { thiss.remove(fieldContainer); }

        var removeFieldIcon = document.createElement('img');
        removeFieldIcon.src = '/static/images/clear.png';
        removeFieldIcon.alt = 'remove';

        removeFieldButton.appendChild(removeFieldIcon);

        return removeFieldButton;
    }

    displayButton()
    {
        console.log('BaseField::displayButton: Unhandled.');
    }

    remove(fieldContainer)
    {
        fieldContainer.remove();
        this.displayButton();
    }
}

class TextInputField
{
    constructor(sheetItem)
    {
        this.sheetItem = sheetItem;
    }

    display(title='')
    {
        var textInput = document.createElement('input');
        textInput.id = 'sheetItemTitle';
        textInput.name = 'title';
        textInput.type = 'text';
        textInput.placeholder = 'Title';
        textInput.autocomplete = 'off';
        if (title)
            textInput.value = title;

        this.sheetItem.div.appendChild(textInput);
    }
}

class TextAreaField
{
    constructor(sheetItem)
    {
        this.sheetItem = sheetItem;
    }

    display(description='')
    {
        var textArea = document.createElement('textarea');
        textArea.name = 'description';
        textArea.rows = 3;
        textArea.placeholder = 'Description';
        if (description)
            textArea.value = description;

        this.sheetItem.div.appendChild(textArea);
    }
}

class PriceField extends BaseField
{
    constructor(sheetItem)
    {
        super();
        this.sheetItem = sheetItem;
        this.fieldFilled = false;
    }

    displayButton()
    {
        if (this.fieldFilled)
        {
            this.fieldFilled = false;
            return;
        }

        var priceFieldButton = document.createElement('button');
        priceFieldButton.id = 'priceButton';
        priceFieldButton.type = 'button';
        var thiss = this;
        priceFieldButton.onclick = function() {
            thiss.display();
            priceFieldButton.remove();
        }
        priceFieldButton.textContent = '$';

        this.sheetItem.fieldOptions.appendChild(priceFieldButton);
        this.priceFieldButton = priceFieldButton;
    }

    display(price)
    {
        if (this.sheetItem.priceFieldIsActive())
        {
            // Price field is already displayed
            return;
        }

        var priceContainer = document.createElement('div');
        priceContainer.className = 'price-container';

        var moneySign = document.createElement('h3');
        moneySign.textContent = '$';
        priceContainer.appendChild(moneySign)

        var priceInput = document.createElement('input');
        priceInput.id = 'sheetItemPrice';
        priceInput.name = 'price';
        priceInput.type = 'number';
        priceInput.step = '0.01';
        priceInput.placeholder = 'Price';
        if (price)
        {
            priceInput.value = price;
            this.fieldFilled = true;
        }
        priceContainer.appendChild(priceInput);

        priceContainer.appendChild(super.buildRemoveFieldButton(priceContainer));

        this.priceContainer = priceContainer;

        this.sheetItem.div.insertBefore(priceContainer, this.sheetItem.div.children[2]);
    }
}

class DatetimeField extends BaseField
{
    constructor(sheetItem)
    {
        super();
        this.sheetItem = sheetItem;
        this.fieldFilled = false;
    }

    displayButton()
    {
        if (this.fieldFilled)
        {
            this.fieldFilled = false;
            return;
        }

        var datetimeFieldButton = document.createElement('button');
        datetimeFieldButton.type = 'button';
        var thiss = this;
        datetimeFieldButton.onclick = function() {
            thiss.display();
            datetimeFieldButton.remove();
        }

        var datetimeFieldIcon = document.createElement('img');
        datetimeFieldIcon.src = '/static/images/clock.png';
        datetimeFieldIcon.alt = 'clock';

        datetimeFieldButton.appendChild(datetimeFieldIcon);

        this.sheetItem.fieldOptions.appendChild(datetimeFieldButton);
    }

    display()
    {
        var datetimesContainer = document.createElement('div');
        datetimesContainer.className = 'datetime-container';

        var startInput = document.createElement('input');
        startInput.type = 'datetime-local';
        datetimesContainer.appendChild(startInput);

        var toWord = document.createElement('h3');
        toWord.textContent = 'to';
        datetimesContainer.appendChild(toWord)

        var endInput = document.createElement('input');
        endInput.type = 'datetime-local';
        datetimesContainer.appendChild(endInput);

        datetimesContainer.appendChild(super.buildRemoveFieldButton(datetimesContainer));
        this.datetimesContainer = datetimesContainer;

        this.sheetItem.div.insertBefore(datetimesContainer, this.sheetItem.div.children[2]);
    }
}

function removeAndRecordPageItemForDeletion(pageItemId, sourceButton)
{
    removePageItem(sourceButton);

    // Record Page ID to be deleted on Page save
    var pageItemIdsToDelete = document.getElementById('pageItemIdsToDelete');
    pageItemIdsToDelete.value += !pageItemIdsToDelete.value ? pageItemId
                                                            : pageItemIdsToDelete.value += `|${pageItemId}`;
}

function removePageItem(sourceButton)
{
    // Remove Page item from page
    // TODO: Removing the first Page item causes an unwanted <hr>
    sourceButton.parentNode.parentNode.remove();
}

function submitPageDeleteForm()
{
    document.getElementById('pageDeleteForm').submit();
}
