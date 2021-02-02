// General popup
var popupContainer = document.getElementById('popupContainer');

popupContainer.onclick = function() {
    dismissPopup();
}

function dismissPopup() {
    popupContainer.style.display = 'none';
    changeEmailPopup.style.display = 'none';
    confirmationPopup.style.display = 'none';
}

// Confirmation popup
var confirmationPopup = document.getElementById('confirmationPopup');

function displayConfirmationPopup(arg) {
    confirmationData = JSON.parse(document.getElementById(arg).textContent);

    document.getElementById('prompt').innerHTML = confirmationData['prompt'];

    var confirmButton = document.getElementById('confirmButton');
    confirmButton.innerHTML = confirmationData['confirmText']
    confirmButton.value = confirmationData['action'];

    popupContainer.style.display = 'flex';
    confirmationPopup.style.display = 'flex';
}

// Email popup
var changeEmailPopup = document.getElementById('changeEmailPopup');

function displayChangeEmailPopup(arg) {
    confirmationData = JSON.parse(document.getElementById(arg).textContent);

    popupContainer.style.display = 'flex';
    changeEmailPopup.style.display = 'flex';
}

changeEmailPopup.addEventListener('click',
                                  function(event) {
    event.stopPropagation();
}, false);


function submitConfirmationForm() {
    document.getElementById('ConfirmationForm').submit();
}
