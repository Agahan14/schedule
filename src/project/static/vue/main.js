const app = Vue.createApp({
    components: {
        CreateEvent,
        BookingList,
        InteractiveCalendar,
    },
    data() {
        return {
            createEventOpened: false,
            bookings: [],
        };
    },
});

app.mount("#app");