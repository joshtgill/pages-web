var popupContainer = document.getElementById('popupContainer');

popupContainer.onclick = function() {
    dismissPopup();
}

function dismissPopup() {
    popupContainer.style.display = 'none';
    confirmationPopup.style.display = 'none';
}

var confirmationPopup = document.getElementById('confirmationPopup');

function displayConfirmationPopup(dataIdentifier) {
    confirmationData = JSON.parse(document.getElementById(dataIdentifier).textContent);
    console.log(confirmationData);

    document.getElementById('prompt').innerHTML = confirmationData['prompt'];

    var confirmButton = document.getElementById('confirmButton');
    confirmButton.innerHTML = confirmationData['confirmButtonText']
    confirmButton.name = confirmationData['formName'];
    confirmButton.value = confirmationData['formValue'];

    popupContainer.style.display = 'flex';
    confirmationPopup.style.display = 'flex';
}

function submitConfirmationForm() {
    document.getElementById('confirmationForm').submit();
}
