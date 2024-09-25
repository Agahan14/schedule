createApp({
    components: {
        CreateEvent,
        CreateAvailability
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
        },
        closeAvailability() {
            this.createAvailabilityOpened = false;
        },
    }
}).mount("#app");
