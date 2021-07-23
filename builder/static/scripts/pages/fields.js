class BaseField {
    constructor(template, isOptional, values) {
        this.isOptional = isOptional;
        this.values = values;

        this.container = null;
        this.buildContainer(template);

        this.button = null;
        if (this.isOptional) {
            this.buildButton();
        }
    }

    buildButton() {
        this.button = document.createElement('button');
        this.button.type = 'button';
        var thiss = this;
        this.button.onclick = function () {
            thiss.toggle(true);
        }
    }

    getButton() {
        return this.button;
    }

    buildContainer(template) {
        this.container = document.createElement('div');
        this.container.className = 'field-container';
        this.container.innerHTML = template;

        this.detailContainer();
    }

    detailContainer() {
        console.log('BaseField::detailContainer(): Unhandled');
    }

    getContainer() {
        return this.container;
    }

    toggle(enable) {
        if (enable) {
            this.container.style.display = 'flex';
            this.button.style.display = 'none';
        }
        else {
            this.button.style.display = 'inline-block';
            this.container.style.display = 'none';

            this.disable();
        }
    }

    buildRemoveFieldButton() {
        var removeFieldButton = document.createElement('button');
        removeFieldButton.id = 'removeFieldButton'
        removeFieldButton.type = 'button';
        var thiss = this;
        removeFieldButton.onclick = function() {
            thiss.toggle(false);
        }

        var removeFieldIcon = document.createElement('img');
        removeFieldIcon.src = '/static/images/clear.png';
        removeFieldIcon.alt = 'remove';

        removeFieldButton.appendChild(removeFieldIcon);

        return removeFieldButton;
    }

    hasPrimaryValues() {
        return this.values[0] != null && this.values[0] != '';
    }

    hasSecondaryValues() {
        return false;
    }

    disable() {
        var inputs = this.container.querySelectorAll('input, textarea');
        console.log(inputs);
        for (var i = 0; i < inputs.length; ++i) {
            inputs[i].value = '';
            inputs[i].required = false;
        }
    }
}


class TextInputField extends BaseField {
    constructor(name, placeholder, ...args) {
        var template = `
            <input type="text" name="${name}" placeholder="${placeholder}" autocomplete="off">
        `
        super(template, false, args);
    }

    detailContainer() {
        this.container.id = 'title-field-container';
        if (this.hasPrimaryValues()) {
            this.container.querySelector('input').value = this.values[0];
        }
    }
}


class TextAreaField extends BaseField {
    constructor(isOptional, ...args) {
        var template = `
            <textarea name="description" rows=3 placeholder="Description"></textarea>
        `
        super(template, isOptional, args);
    }

    buildButton() {
        super.buildButton();
        this.button.innerHTML = '<img src="/static/images/text.png" alt="text icon">';
    }

    detailContainer() {
        if (this.hasPrimaryValues()) {
            this.container.querySelector('textarea').value = this.values[0];
        }

        if (this.isOptional) {
            this.container.appendChild(super.buildRemoveFieldButton());
        }
    }
}


class LocationField extends BaseField {
    constructor(isOptional, ...args) {
        var template = `
            <img src="/static/images/location.png" alt="location icon">
            <input type="text" name="location" placeholder="Location" autocomplete="off" required>
        `
        super(template, isOptional, args);
    }

    buildButton() {
        super.buildButton();
        this.button.innerHTML = '<img src="/static/images/location.png" alt="location icon">';
    }

    detailContainer() {
        this.container.id = 'location-field-container';

        if (this.hasPrimaryValues()) {
            this.container.querySelector('input').value = this.values[0];
        }

        if (this.isOptional) {
            this.container.appendChild(super.buildRemoveFieldButton());
        }
    }
}


class DatetimeField extends BaseField {
    constructor(isOptional, ...args) {
        var template = `
            <div class="datetime-header">
                <img src="/static/images/datetime.png" alt="clock icon">
                <div class="toggle">
                    <h4>Repeat</h4>
                    <label class="switch">
                        <input type="checkbox" name="repeat">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
            <div class="datetime-range">
                <input type="datetime-local" name="startDatetime" required>
                <h3>to</h3>
                <input type="datetime-local" name="endDatetime" required>
            </div>
            <div class="datetime-repeat">
                <div class="days">
                    <input type="hidden" id="selectedDaysInput" name="selectedDays">
                    <button type="button" class="day-button" name="monday">M</button>
                    <button type="button" class="day-button" name="tuesday">T</button>
                    <button type="button" class="day-button" name="wednesday">W</button>
                    <button type="button" class="day-button" name="thursday">TH</button>
                    <button type="button" class="day-button" name="friday">F</button>
                    <button type="button" class="day-button" name="saturday">S</button>
                    <button type="button" class="day-button" name="sunday">SU</button>
                </div>
                <div class="times">
                    <input type="time" name="startTime" required>
                    <h3>to</h3>
                    <input type="time" name="endTime" required>
                </div>
                <div class="times">
                    <h3>starting on</h3>
                    <input type="date" name="startDate" required>
                    <h3>ending on</h3>
                    <input type="date" name="endDate" required>
                </div>
            </div>
        `
        super(template, isOptional, args);
    }

    buildButton() {
        super.buildButton();
        this.button.innerHTML = '<img src="/static/images/datetime.png" alt="clock icon">';
    }

    detailContainer() {
        this.container.id = 'datetime-field-container';

        if (this.isOptional) {
            this.container.querySelector('.datetime-header').appendChild(this.buildRemoveFieldButton());
        }

        var datetimeRangeContainer = this.container.querySelector('.datetime-range');
        var datetimeRepeatContainer = this.container.querySelector('.datetime-repeat');
        var repeatToggleInput = this.container.querySelector('input[name="repeat"]');
        repeatToggleInput.onchange = function() {
            if (this.checked) {
                datetimeRangeContainer.style.display = 'none';
                var datetimeRangeInputs = datetimeRangeContainer.querySelectorAll('input');
                for (var i = 0; i < datetimeRangeInputs.length; ++i) {
                    datetimeRangeInputs[i].required = false;
                    datetimeRangeInputs[i].value = '';
                }

                datetimeRepeatContainer.style.display = 'flex';
                var datetimeRepeatInputs = datetimeRepeatContainer.querySelectorAll('input');
                for (var i = 0; i < datetimeRepeatInputs.length; ++i) {
                    datetimeRepeatInputs[i].required = true;
                }
            }
            else {
                datetimeRangeContainer.style.display = 'flex';
                var datetimeRangeInputs = datetimeRangeContainer.querySelectorAll('input');
                for (var i = 0; i < datetimeRangeInputs.length; ++i) {
                    datetimeRangeInputs[i].required = true;
                }

                datetimeRepeatContainer.style.display = 'none';
                var datetimeRepeatInputs = datetimeRepeatContainer.querySelectorAll('input');
                for (var i = 0; i < datetimeRepeatInputs.length; ++i) {
                    datetimeRepeatInputs[i].required = false;
                    datetimeRepeatInputs[i].value = '';
                }
                var datetimeRepeatDayButtons = datetimeRepeatContainer.querySelectorAll('button');
                for (var i = 0; i < datetimeRepeatDayButtons.length; ++i) {
                    if (datetimeRepeatDayButtons[i].value) {
                        datetimeRepeatDayButtons[i].click();
                    }
                }
            }
        }
        repeatToggleInput.checked = this.hasSecondaryValues();
        repeatToggleInput.dispatchEvent(new Event('change'));

        var selectedDays = []
        var selectedDaysInput = this.container.querySelector('#selectedDaysInput');
        var dayButtons = this.container.querySelectorAll('.day-button');
        for (var i = 0; i < dayButtons.length; i++) {
            dayButtons[i].onclick = function() {
                if (this.value) {
                    // Button is selected, unselect it.
                    selectedDays.splice(selectedDays.indexOf(this.textContent), 1);
                    this.style.border = 'none';
                    this.value = false;
                }
                else {
                    // Button is not selected, select it.
                    selectedDays.push(this.textContent);
                    this.style.border = '2px solid rgb(0, 91, 255)';
                    this.value = true;
                }
                selectedDaysInput.value = selectedDays.join('|');
            }
        }

        if (this.hasPrimaryValues()) {
            this.container.querySelector('input[name="startDatetime"]').value = this.values[0]['startDatetime'];
            this.container.querySelector('input[name="endDatetime"]').value = this.values[0]['endDatetime'];
        }
        else if (this.hasSecondaryValues()) {
            var daysInWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
            for (var index in daysInWeek) {
                if (this.values[1][daysInWeek[index]]) {
                    this.container.querySelector(`button[name="${daysInWeek[index]}"]`).click();
                }
            }
            this.container.querySelector('input[name="startTime"]').value = this.values[1]['startTime'];
            this.container.querySelector('input[name="endTime"]').value = this.values[1]['endTime'];
            this.container.querySelector('input[name="startDate"]').value = this.values[1]['startDate'];
            this.container.querySelector('input[name="endDate"]').value = this.values[1]['endDate'];
        }
    }

    hasPrimaryValues() {
        return this.values[0] != null && this.values[0] != '';
    }

    hasSecondaryValues() {
        return this.values[1] != null && this.values[1] != '';
    }

    disable() {
        super.disable();

        var repeatDayButtons = this.container.querySelector('.datetime-repeat').querySelectorAll('button');
        for (var i = 0; i < repeatDayButtons.length; ++i) {
            if (repeatDayButtons[i].value) {
                repeatDayButtons[i].click();
            }
        }
    }
}


class PriceField extends BaseField {
    constructor(isOptional, ...args) {
        var template = `
            <img src="/static/images/price.png" alt="price icon">
            <input type="number" step="0.01" id="sheetItemPrice" name="price" placeholder="Price">
        `
        super(template, isOptional, args);
    }

    buildButton() {
        super.buildButton();
        this.button.innerHTML = '<img src="/static/images/price.png" alt="price icon">';
    }

    detailContainer() {
        this.container.id = 'price-field-container';
        this.container.appendChild(super.buildRemoveFieldButton());

        if (this.hasPrimaryValues()) {
            this.container.querySelector('input').value = this.values[0];
        }
    }
}


class ToggleField extends BaseField {
    constructor(...args) {
        var template = `
            <div class="toggle">
                <h4>Public attendance</h4>
                <label class="switch">
                    <input type="checkbox" name="attendanceIsPublic">
                    <span class="slider"></span>
                </label>
            </div>
        `
        super(template, false, args);
    }

    detailContainer() {
        this.container.id = 'toggle-field-container';

        if (this.hasPrimaryValues()) {
            this.container.querySelector('input[name="attendanceIsPublic"]').checked = true;
        }
    }
}
