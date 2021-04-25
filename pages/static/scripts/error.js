class Error {
    constructor() {
        this.container = document.getElementById('errorContainer');
        this.message = document.getElementById('errorMessage');
        this.link = document.getElementById('errorLink');
    }

    display(errorData) {
        this.message.innerHTML = errorData['error']['message'];
        if (errorData['error']['link']) {
            this.link.href = errorData['error']['link']['path'];
            this.link.innerHTML = errorData['error']['link']['text'];
        }
        this.container.style.display = 'flex';
    }

    hide() {
        this.container.style.display = 'none';
    }
}

window.onbeforeunload = function() {
    error.hide();
}

error = new Error();
