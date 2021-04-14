class Eventt {
    constructor(div, dataIdentifier=null) {
        this.container = div;

        var data = {}
        if (dataIdentifier) {
            data = JSON.parse(document.getElementById(dataIdentifier).textContent);
        }
        this.fields = [new TextAreaField(data['description']),
                       new LocationField(false, data['location']),
                       new DatetimeField(false, data['singleOccurence'], data['repeatingOccurence']),
                       new ToggleField(data['attendanceIsPublic'])];

        this.buildContainer();
    }

    buildContainer() {
        for (var index in this.fields) {
            this.container.appendChild(this.fields[index].getContainer());
        }
    }
}
