var popupContainer = document.getElementById('popupContainer');

popupContainer.onclick = function() {
    dismissPopup();
}

function dismissPopup() {
    popupContainer.style.display = 'none';
    changeEmailPopup.style.display = 'none';
    confirmationPopup.style.display = 'none';
}

var changeEmailPopup = document.getElementById('changeEmailPopup');

function displayChangeEmailPopup() {
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
