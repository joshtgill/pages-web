function displayEmptySheetItem()
{
    var items = document.getElementById('items');

    if (items.childElementCount)
        items.appendChild(document.createElement('hr'));

    var item = document.createElement('div');
    item.className = 'item';

    idInput = document.createElement('input');
    idInput.className = 'hidden';
    idInput.name = 'id';
    idInput.value = '-1';
    item.appendChild(idInput);

    titleInput = document.createElement('input');
    titleInput.id = 'sheetItemTitle';
    titleInput.name = 'title';
    titleInput.type = 'text';
    titleInput.placeholder = 'Title';
    titleInput.autocomplete = 'off';
    item.appendChild(titleInput);

    descriptionTextArea = document.createElement('textarea');
    descriptionTextArea.name = 'description';
    descriptionTextArea.rows = 3;
    descriptionTextArea.placeholder = 'Description';
    item.appendChild(descriptionTextArea);

    priceInput = document.createElement('input');
    priceInput.id = 'sheetItemPrice';
    priceInput.name = 'price';
    priceInput.type = 'number';
    priceInput.step = '0.01';
    priceInput.placeholder = 'Price';
    item.appendChild(priceInput);

    items.appendChild(item);
}

function createAndSubmitDeleteForm(sheetId, sheetItemId)
{
    document.getElementById('deleteSheetIdInput').setAttribute('value', sheetId);
    document.getElementById('deleteSheetItemIdInput').setAttribute('value', sheetItemId);
    document.getElementById('deleteForm').submit();
}
