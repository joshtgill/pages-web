var popupContainer = document.getElementById('popupContainer');
var confirmButton = document.getElementById('confirmButton');


function displayConfirmationPopup(arg) {
    confirmationData = JSON.parse(document.getElementById(arg).textContent);

    document.getElementById('confirmMessage').innerHTML = confirmationData['message'];
    confirmButton.innerHTML = confirmationData['buttonText']
    confirmButton.value = confirmationData['action'];
    if (confirmButton.value == 'DELETE_ACCOUNT') {
        confirmButton.style.backgroundColor = 'rgb(235, 70, 70)'
        confirmButton.style.border = '2px solid rgb(235, 70, 70)'
    }
    else {
        confirmButton.style.backgroundColor = 'rgb(30, 30, 30)';
        confirmButton.style.border = '2px solid rgb(30, 30, 30)';
    }
    popupContainer.style.display = 'flex';
}

function hidePopupContainer() {
    popupContainer.style.display = 'none';
}

popupContainer.onclick = function() {
    hidePopupContainer();
}

function submitProfileForm() {
    document.getElementById('profileForm').submit();
}
