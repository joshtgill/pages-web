class BasePopup
{
    constructor(popupContainer, popup, form)
    {
        this.popupContainer = popupContainer;
        this.popup = popup;
        this.form = form;
    }

    display()
    {
        this.popup.appendChild(this.form);

        this.popupContainer.style.display = 'flex';
        this.popup.style.display = 'flex';
        this.form.style.display = 'flex';
    }

    dismiss()
    {
        this.popupContainer.style.display = 'none';
        this.popup.style.display = 'none';
        this.form.style.display = 'none';
    }

    submitForm()
    {
        this.form.submit();
    }
}
