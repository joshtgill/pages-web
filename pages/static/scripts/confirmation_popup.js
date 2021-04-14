class ConfirmationPopup extends BasePopup
{
    constructor(popupContainer, popup, confirmationForm)
    {
        super(popupContainer, popup, confirmationForm);
    }

    display(prompt, confirmButtonText, formName, formValue, dismissButtonText='Back', dismissRedirectLink=null) {
        document.getElementById('prompt').innerHTML = prompt;
        var confirmButton = document.getElementById('confirmButton');
        confirmButton.innerHTML = confirmButtonText;
        confirmButton.name = formName;
        confirmButton.value = formValue;
        document.getElementById('dismissButton').innerHTML = dismissButtonText;
        this.dismissRedirectLink = dismissRedirectLink;

        super.display();
    }

    dismiss()
    {
        if (this.dismissRedirectLink)
            window.location.href = this.dismissRedirectLink;
        else
            super.dismiss();
    }
}

confirmationPopup = new ConfirmationPopup(document.getElementById('popupContainer'),
                                          document.getElementById('popup'),
                                          document.getElementById('confirmationForm'));
