function selectColorOption(colorContainer) {
    var button = colorContainer.childNodes[1];
    console.log(button);

    // Unselect all
    var colorContainers = document.getElementById('colors').querySelectorAll('.color-container');
    for (var i = 0; i < colorContainers.length; ++i) {
        colorContainers[i].style.borderColor = 'rgb(250, 250, 252)';
    }

    colorContainer.style.borderColor = 'rgb(0, 123, 224)';
    document.getElementById('organizationColorInput').value = button.value;
}

function josh() {
    console.log('josh');
}