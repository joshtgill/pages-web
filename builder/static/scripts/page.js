function displayEmptySheetItem()
{
    var items = document.getElementById('items');

    var item = document.createElement('div');
    item.className = 'item';

    if (items.childElementCount)
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
    removeButton.onclick = function() { removePageItem(this); }
    removeButton.textContent = 'Remove item'
    item.appendChild(removeButton);

    items.appendChild(item);
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
    sourceButton.parentNode.remove();
}

function submitPageDeleteForm()
{
    document.getElementById('pageDeleteForm').submit();
}
