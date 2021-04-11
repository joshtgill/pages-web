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
            thiss.updateVisibility(true);
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

    hasPrimaryValues() {
        return this.values[0] != null && this.values[0] != '';
    }

    hasSecondaryValues() {
        return false;
    }

    nullValues() {
        console.log('BaseField::nullValues(): Unhandled');
    }
}


class TextInputField extends BaseField {
    constructor(...args) {
        var template = `
            <input type="text" name="title" placeholder="Title" autocomplete="off">
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
    constructor(...args) {
        var template = `
            <textarea name="description" rows=3 placeholder="Description"></textarea>
        `
        super(template, false, args);
    }

    detailContainer() {
        if (this.hasPrimaryValues()) {
            this.container.querySelector('textarea').value = this.values[0];
        }
    }
}


class LocationField extends BaseField {
    constructor(isOptional, ...args) {
        var template = `
            <img src="/static/images/location.png" alt="location icon">
            <input type="text" name="location" placeholder="Location" autocomplete="off">
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

    nullValues() {
        this.container.querySelector('input[name="location"]').value = '';
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
    }

    nullValues() {
        this.container.querySelector('#sheetItemPrice').value = '';
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
