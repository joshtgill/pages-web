class Eventt {
    constructor(div, dataIdentifier=null) {
        this.container = div;

        var data = {}
        if (dataIdentifier) {
            data = JSON.parse(document.getElementById(dataIdentifier).textContent);
        }

        this.baseFields = [new TextAreaField(data['description']),
                           new LocationField(false, data['location']),
                           new DatetimeField(false, data['startDatetime'], data['endDatetime'], data['repeating'])];
        this.buildContainer(data['attendanceIsPublic']);
    }

    buildContainer(attendanceIsPublic) {
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
        toggleInput.checked = attendanceIsPublic;
        switchh.appendChild(toggleInput);

        var span = document.createElement('span');
        span.className = 'slider';
        switchh.appendChild(span);

        toggle.appendChild(switchh);
        this.container.appendChild(toggle);
    }
}
