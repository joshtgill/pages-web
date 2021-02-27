class ConfirmationPopup extends BasePopup
{
    constructor(popupContainer, popup, confirmationForm)
    {
        super(popupContainer, popup, confirmationForm);
    }

    display(dataIdentifier)
    {
        var confirmationData = JSON.parse(document.getElementById(dataIdentifier).textContent);

        document.getElementById('prompt').innerHTML = confirmationData['prompt'];

        var confirmButton = document.getElementById('confirmButton');
        confirmButton.innerHTML = confirmationData['confirmButtonText']
        confirmButton.name = confirmationData['formName'];
        confirmButton.value = confirmationData['formValue'];

        super.display();
    }

    dismiss()
    {
        super.dismiss();
    }
}

confirmationPopup = new ConfirmationPopup(document.getElementById('popupContainer'),
                                          document.getElementById('popup'),
                                          document.getElementById('confirmationForm'));
