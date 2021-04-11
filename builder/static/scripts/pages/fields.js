class BaseField {
    constructor(container, values) {
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
        super(container, values);
        this.button = button;

        this.buildButton();
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
        removeFieldButton.onclick = function () {
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
        super(document.createElement('div'), args);
    }

    buildContainer() {
        this.container.className = 'field-container';
        this.container.id = 'title-field-container';

        var titleInput = document.createElement('input');
        titleInput.name = 'title';
        titleInput.type = 'text';
        titleInput.placeholder = 'Title';
        titleInput.autocomplete = 'off';
        titleInput.value = this.hasPrimaryValues() ? this.values[0] : '';

        this.container.appendChild(titleInput);
    }
}


class TextAreaField extends BaseField {
    constructor(...args) {
        super(document.createElement('div'), args);
    }

    buildContainer() {
        this.container.className = 'field-container';

        var descriptionTextArea = document.createElement('textarea');
        descriptionTextArea.name = 'description';
        descriptionTextArea.rows = 3;
        descriptionTextArea.placeholder = 'Description';
        descriptionTextArea.value = this.hasPrimaryValues() ? this.values[0] : '';

        this.container.appendChild(descriptionTextArea);
    }
}


class LocationField extends BaseOptionalField {
    constructor(...args) {
        super(document.createElement('button'), document.createElement('div'), args);
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

        var locationIcon = document.createElement('img');
        locationIcon.src = '/static/images/location.png';
        locationIcon.alt = 'price';
        this.container.appendChild(locationIcon);

        var locationInput = document.createElement('input');
        locationInput.name = 'location';
        locationInput.type = 'text';
        locationInput.placeholder = 'Location';
        locationInput.autocomplete = 'off';
        locationInput.value = this.hasPrimaryValues() ? this.values[0] : '';
        this.container.appendChild(locationInput);

        this.container.appendChild(super.buildRemoveFieldButton());
    }

    nullValues() {
        this.container.querySelector('input[name="location"]').value = '';
    }
}


class DatetimeField extends BaseOptionalField {
    constructor(...args) {
        super(document.createElement('button'), document.createElement('div'), args);
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

        var datetimeRange = document.createElement('div');
        var datetimeRepeat = document.createElement('div');

        // Datetime header
        var datetimeHeader = document.createElement('div');
        datetimeHeader.className = 'datetime-header';

        var datetimeFieldIcon = document.createElement('img');
        datetimeFieldIcon.src = '/static/images/datetime.png';
        datetimeFieldIcon.alt = 'clock';
        datetimeHeader.appendChild(datetimeFieldIcon);

        // Toggle
        var toggle = document.createElement('div');
        toggle.className = 'toggle';

        var label = document.createElement('h4');
        label.textContent = 'Repeat';
        toggle.appendChild(label);

        var switchh = document.createElement('label');
        switchh.className = 'switch';

        var toggleInput = document.createElement('input');
        toggleInput.type = 'checkbox';
        toggleInput.name = 'repeate';
        toggleInput.onchange = function() {
            if (this.checked) {
                datetimeRange.style.display = 'none';
                datetimeRepeat.style.display = 'flex';
            }
            else {
                datetimeRange.style.display = 'flex';
                datetimeRepeat.style.display = 'none';
            }
        }
        switchh.appendChild(toggleInput);

        var span = document.createElement('span');
        span.className = 'slider';
        switchh.appendChild(span);

        toggle.appendChild(switchh);
        datetimeHeader.appendChild(toggle);

        // Remove field button
        datetimeHeader.appendChild(super.buildRemoveFieldButton());

        this.container.appendChild(datetimeHeader);

        // Datetime range
        datetimeRange.className = 'datetime-range';

        var startDatetimeInput = document.createElement('input');
        startDatetimeInput.type = 'datetime-local';
        startDatetimeInput.name = 'startDatetime';
        startDatetimeInput.value = this.hasPrimaryValues() ? this.values[0] : '';
        datetimeRange.appendChild(startDatetimeInput);

        var toLabel = document.createElement('h3');
        toLabel.textContent = 'to';
        datetimeRange.appendChild(toLabel);

        var endDatetimeInput = document.createElement('input');
        endDatetimeInput.type = 'datetime-local';
        endDatetimeInput.name = 'endDatetime';
        endDatetimeInput.value = this.hasPrimaryValues() ? this.values[1] : '';
        datetimeRange.appendChild(endDatetimeInput);

        this.container.appendChild(datetimeRange);

        // Datetime repeat
        datetimeRepeat.className = 'datetime-repeat';
        datetimeRepeat.style.display = 'none';

        var datetimeRepeatDays = document.createElement('div');
        datetimeRepeatDays.className = 'days';
        var selectedDaysInput = document.createElement('input');
        selectedDaysInput.type = 'hidden';
        selectedDaysInput.name = 'selectedDays';
        var selectedDays = [];
        var dayTexts = ['M', 'T', 'W', 'TH', 'F', 'S', 'SU'];
        var dayNames = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        var dayValues = [false, false, false, false, false, false, false];
        if (this.hasSecondaryValues()) {
            dayValues = [this.values[2]['monday'], this.values[2]['tuesday'], this.values[2]['wednesday'],
                         this.values[2]['thursday'], this.values[2]['friday'], this.values[2]['saturday'], this.values[2]['sunday']];
        }
        for (var i = 0; i < 7; i++) {
            var dayButton = document.createElement('button');
            dayButton.type = 'button';
            dayButton.id = 'dayButton';
            dayButton.textContent = dayTexts[i];
            dayButton.name = dayNames[i];
            dayButton.value = dayValues[i];
            if (dayButton.value == 'true') {
                selectedDays.push(dayButton.textContent);
                selectedDaysInput.value = selectedDays.join('|');
                dayButton.style.border = '2px solid rgb(0, 91, 255)';
            }
            dayButton.onclick = function() {
                if (this.value == 'false') {
                    // Button is 'off', turn it 'on'
                    selectedDays.push(this.textContent);
                    this.style.border = '2px solid rgb(0, 91, 255)';
                    this.value = 'true';
                }
                else {
                    // Button is 'on', turn it 'off'
                    selectedDays.splice(selectedDays.indexOf(this.textContent), 1);
                    this.style.border = 'none';
                    this.value = 'false';
                }
                selectedDaysInput.value = selectedDays.join('|');
                console.log(selectedDaysInput.value);
            }
            datetimeRepeatDays.appendChild(dayButton);
        }
        datetimeRepeat.appendChild(datetimeRepeatDays);
        datetimeRepeat.appendChild(selectedDaysInput);

        var datetimeRepeatTimes = document.createElement('div');
        datetimeRepeatTimes.className = 'times';

        var startTimeInput = document.createElement('input');
        startTimeInput.type = 'time';
        startTimeInput.name = 'startTime';
        startTimeInput.value = this.hasSecondaryValues() ? this.values[2]['startTime'] : '';
        datetimeRepeatTimes.appendChild(startTimeInput);

        var toLabel = document.createElement('h3');
        toLabel.textContent = 'to';
        datetimeRepeatTimes.appendChild(toLabel);

        var endTimeInput = document.createElement('input');
        endTimeInput.type = 'time';
        endTimeInput.name = 'endTime';
        endTimeInput.value = this.hasSecondaryValues() ? this.values[2]['endTime'] : '';
        datetimeRepeatTimes.appendChild(endTimeInput);

        datetimeRepeat.appendChild(datetimeRepeatTimes);

        var datetimeRepeatDates = document.createElement('div');
        datetimeRepeatDates.className = 'times';

        var startingOnLabel = document.createElement('h3');
        startingOnLabel.textContent = 'starting on';
        datetimeRepeatDates.appendChild(startingOnLabel);

        var startDateInput = document.createElement('input');
        startDateInput.type = 'date';
        startDateInput.name = 'startDate';
        startDateInput.value = this.hasSecondaryValues() ? this.values[2]['startDate'] : '';
        datetimeRepeatDates.appendChild(startDateInput);

        datetimeRepeat.appendChild(datetimeRepeatDates);

        var endingOnLabel = document.createElement('h3');
        endingOnLabel.textContent = 'ending on';
        datetimeRepeatDates.appendChild(endingOnLabel);

        var endDateInput = document.createElement('input');
        endDateInput.type = 'date';
        endDateInput.name = 'endDate';
        endDateInput.value = this.hasSecondaryValues() ? this.values[2]['endDate'] : '';
        datetimeRepeatDates.appendChild(endDateInput);

        datetimeRepeat.appendChild(datetimeRepeatDates);

        this.container.appendChild(datetimeRepeat);

        if (this.hasSecondaryValues()) {
            toggleInput.checked = true;
            toggleInput.dispatchEvent(new Event('change'));
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
