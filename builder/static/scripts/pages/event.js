class Eventt {
    constructor(div, dataIdentifier=null) {
        this.container = div;

        var data = {}
        if (dataIdentifier) {
            data = JSON.parse(document.getElementById(dataIdentifier).textContent);
        }

        this.baseFields = [new TextAreaField(data['description']),
                           new LocationField(false, data['location']),
                           new DatetimeField(false, data['startDatetime'], data['endDatetime'], data['repeating']),
                           new ToggleField(data['attendanceIsPublic'])];
        this.buildContainer();
    }

    buildContainer() {
        for (var index in this.baseFields) {
            this.container.appendChild(this.baseFields[index].getContainer());
        }
    }
}
