function displayEmptySheetItem()
{
    var items = document.getElementById('items');

    var item = document.createElement('div');
    item.className = 'item';

    item.appendChild(document.createElement('hr'));

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

    removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.onclick = function() { removeSheetItem(this); }
    removeButton.textContent = 'Remove item'
    item.appendChild(removeButton);

    items.appendChild(item);
}

function removeAndRecordSheetItemForDeletion(sheetItemId, sourceButton)
{
    removeSheetItem(sourceButton);

    // Record Sheet ID to be deleted on Sheet save
    var sheetItemIdsToDelete = document.getElementById('sheetItemIdsToDelete');
    sheetItemIdsToDelete.value += !sheetItemIdsToDelete.value ? sheetItemId
                                                              : sheetItemIdsToDelete.value += `|${sheetItemId}`;
}

function removeSheetItem(sourceButton)
{
    // Remove Sheet item from page
    // TODO: Removing the first Sheet item causes an unwanted <hr>
    sourceButton.parentNode.remove();
}

function submitSheetDeleteForm()
{
    document.getElementById('sheetDeleteForm').submit();
}
