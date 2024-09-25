createApp({
    components: {
        CreateEvent,
        CreateAvailability,
    },
    data() {
        return {
            createEventOpened: false,
            createAvailabilityOpened: false,
        };
    },
    methods: {
        createAvailability() {
            this.createAvailabilityOpened = true;
            console.log("Here");
            console.log(this.createAvailabilityOpened);
        },
        closeAvailability() {
            this.createAvailabilityOpened = false;
        },
    },
}).mount("#app");
