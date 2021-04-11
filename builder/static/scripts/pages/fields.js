class BaseField {
    constructor(isOptional, container, values) {
        this.isOptional = isOptional;
        this.container = container;
        this.values = values;

        this.buildContainer();
    }

    buildContainer() {
        console.log('BaseField::buildContainer(): Unhandled');
    }

    getContainer() {
        return this.container;
    }

    hasPrimaryValues() {
        return this.values[0] != null && this.values[0] != '';
    }

    hasSecondaryValues() {
        return false;
    }
}


class BaseOptionalField extends BaseField {
    constructor(button, container, values) {
        super(button != null, container, values);
        if (button != null) {
            this.button = button;
            this.buildButton();
        }
        else {
            this.button = null;
        }
    }

    buildButton() {
        this.button.type = 'button';
        var thiss = this;
        this.button.onclick = function () {
            thiss.updateVisibility(true);
        }
    }

    getButton() {
        return this.button;
    }

    buildRemoveFieldButton() {
        var removeFieldButton = document.createElement('button');
        removeFieldButton.type = 'button';
        var thiss = this;
        removeFieldButton.onclick = function() {
            thiss.updateVisibility(false);
        }

        var removeFieldIcon = document.createElement('img');
        removeFieldIcon.src = '/static/images/clear.png';
        removeFieldIcon.alt = 'remove';

        removeFieldButton.appendChild(removeFieldIcon);

        return removeFieldButton;
    }

    updateVisibility(container) {
        if (container) {
            this.container.style.display = 'flex';
            this.button.style.display = 'none';
        }
        else {
            this.button.style.display = 'inline-block';
            this.container.style.display = 'none';

            this.nullValues();
        }
    }

    nullValues() {
        console.log('BaseOptionalField::nullValues(): Unhandled');
    }
}


class TextInputField extends BaseField {
    constructor(...args) {
        super(false, document.createElement('div'), args);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'title-field-container';

        var template = `
            <input type="text" name="title" placeholder="Title" autocomplete="off">
        `
        this.container.innerHTML = template;
    }
}


class TextAreaField extends BaseField {
    constructor(...args) {
        super(false, document.createElement('div'), args);
    }

    buildContainer() {
        this.container.className = 'field-container';

        var template = `
            <textarea name="description" rows=3 placeholder="Description"></textarea>
        `

        this.container.innerHTML = template;

        if (this.hasPrimaryValues()) {
            this.container.querySelector('textarea').value = this.values[0];
        }
    }
}


class LocationField extends BaseOptionalField {
    constructor(isOptional, ...args) {
        super(isOptional ? document.createElement('button') : null, document.createElement('div'), args);
    }

    buildButton() {
        super.buildButton();

        var locationFieldIcon = document.createElement('img');
        locationFieldIcon.src = '/static/images/location.png';
        locationFieldIcon.alt = 'location';

        this.button.appendChild(locationFieldIcon);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'location-field-container';

        var template = `
            <img src="/static/images/location.png" alt="location icon">
            <input type="text" name="location" placeholder="Location" autocomplete="off">
        `
        this.container.innerHTML = template;

        if (this.hasPrimaryValues()) {
            this.container.querySelector('input').value = this.values[0];
        }

        if (this.isOptional) {
            this.container.appendChild(super.buildRemoveFieldButton());
        }
    }

    nullValues() {
        this.container.querySelector('input[name="location"]').value = '';
    }
}

class DatetimeField extends BaseOptionalField {
    constructor(isOptional, ...args) {
        super(isOptional ? document.createElement('button') : null, document.createElement('div'), args);
    }

    buildButton() {
        super.buildButton();

        var datetimeFieldIcon = document.createElement('img');
        datetimeFieldIcon.src = '/static/images/datetime.png';
        datetimeFieldIcon.alt = 'clock';

        this.button.appendChild(datetimeFieldIcon);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'datetime-field-container';

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
                <input type="datetime-local" name="startDatetime">
                <h3>to</h3>
                <input type="datetime-local" name="endDatetime">
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
                    <input type="time" name="startTime">
                    <h3>to</h3>
                    <input type="time" name="endTime">
                </div>
                <div class="times">
                    <h3>starting on</h3>
                    <input type="date" name="startDate">
                    <h3>ending on</h3>
                    <input type="date" name="endDate">
                </div>
            </div>
        `
        this.container.innerHTML = template;

        if (this.isOptional) {
            this.container.querySelector('.datetime-header').appendChild(this.buildRemoveFieldButton());
        }

        var datetimeRangeContainer = this.container.querySelector('.datetime-range');
        var datetimeRepeatContainer = this.container.querySelector('.datetime-repeat');
        var repeatToggleInput = this.container.querySelector('input[name="repeat"]');
        repeatToggleInput.onchange = function() {
            if (this.checked) {
                datetimeRangeContainer.style.display = 'none';
                datetimeRepeatContainer.style.display = 'flex';
            }
            else {
                datetimeRangeContainer.style.display = 'flex';
                datetimeRepeatContainer.style.display = 'none';
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
            this.container.querySelector('input[name="startDatetime"]').value = this.values[0];
            this.container.querySelector('input[name="endDatetime"]').value = this.values[1];
        }
        else if (this.hasSecondaryValues()) {
            var daysInWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
            for (var index in daysInWeek) {
                if (this.values[2][daysInWeek[index]]) {
                    this.container.querySelector(`button[name="${daysInWeek[index]}"]`).dispatchEvent(new Event('click'))
                }
            }
            this.container.querySelector('input[name="startTime"]').value = this.values[2]['startTime'];
            this.container.querySelector('input[name="endTime"]').value = this.values[2]['endTime'];
            this.container.querySelector('input[name="startDate"]').value = this.values[2]['startDate'];
            this.container.querySelector('input[name="endDate"]').value = this.values[2]['endDate'];
        }
    }

    hasPrimaryValues() {
        return this.values[0] != null || this.values[1] != null;
    }

    hasSecondaryValues() {
        return this.values[2];
    }

    nullValues() {
        this.container.querySelector('input[name="startDatetime"]').value = '';
        this.container.querySelector('input[name="endDatetime"]').value = '';
        this.container.querySelector('input[name="startTime"]').value = '';
        this.container.querySelector('input[name="endTime"]').value = '';
        this.container.querySelector('input[name="startDate"]').value = '';
        this.container.querySelector('input[name="endDate"]').value = '';
        this.container.querySelector('input[name="selectedDays"]').value = '';
    }
}
