var popupContainer = document.getElementById('popupContainer');
var confirmButton = document.getElementById('confirmButton');


function displayConfirmationPopup(arg) {
    confirmationData = JSON.parse(document.getElementById(arg).textContent);

    document.getElementById('confirmMessage').innerHTML = confirmationData['message'];
    confirmButton.innerHTML = confirmationData['buttonText']
    confirmButton.value = confirmationData['action'];
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
