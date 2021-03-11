class ConfirmationPopup extends BasePopup
{
    constructor(popupContainer, popup, confirmationForm)
    {
        super(popupContainer, popup, confirmationForm);
    }

    display(dataIdentifier, dismissLink=null)
    {
        var confirmationData = JSON.parse(document.getElementById(dataIdentifier).textContent);
        this.dismissLink = dismissLink;

        document.getElementById('prompt').innerHTML = confirmationData['prompt'];

        var confirmButton = document.getElementById('confirmButton');
        confirmButton.innerHTML = confirmationData['confirmButtonText']
        confirmButton.name = confirmationData['formName'];
        confirmButton.value = confirmationData['formValue'];
        document.getElementById('dismissButton').innerHTML = confirmationData['dismissButtonText']

        super.display();
    }

    dismiss()
    {
        if (this.dismissLink)
            window.location.href = this.dismissLink;
        else
            super.dismiss();
    }
}

confirmationPopup = new ConfirmationPopup(document.getElementById('popupContainer'),
                                          document.getElementById('popup'),
                                          document.getElementById('confirmationForm'));
