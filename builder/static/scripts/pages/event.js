class Event {
    constructor(div) {
        this.container = div;

        this.baseFields = [new TextAreaField(), new LocationField(false), new DatetimeField(false)];
        this.buildContainer();
    }

    loadItems(dataIdentifier) {
        var items = JSON.parse(document.getElementById(dataIdentifier).textContent);
        for (var index in items) {
            this.displayItem(items[index]);
        }
    }

    buildContainer() {
        for (var index in this.baseFields) {
            this.container.appendChild(this.baseFields[index].getContainer());
        }

        var toggle = document.createElement('div');
        toggle.className = 'toggle';
        toggle.id = "publicAttendance";

        var label = document.createElement('h4');
        label.textContent = 'Public attendance';
        toggle.appendChild(label);

        var switchh = document.createElement('label');
        switchh.className = 'switch';

        var toggleInput = document.createElement('input');
        toggleInput.type = 'checkbox';
        toggleInput.name = 'attendanceIsPublic';
        switchh.appendChild(toggleInput);

        var span = document.createElement('span');
        span.className = 'slider';
        switchh.appendChild(span);

        toggle.appendChild(switchh);
        this.container.appendChild(toggle);
    }
}
