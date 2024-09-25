const { defineComponent, createApp } = Vue;

const BookingList = defineComponent({
    props: ["bookings"],
    template: "#bookings-template",
    methods: {
        async cancelBooking(bookingId) {
            try {
                const response = await fetch(`/booking/cancel/${bookingId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    this.$emit("booking-canceled", bookingId);
                } else {
                    console.error("Не удалось отменить бронирование:", response.statusText);
                }
            } catch (error) {
                console.error("Ошибка отмены бронирования:", error.message);
            }
        },
    },
});

const app = Vue.createApp({
    components: {
        BookingList,
    },
    data() {
        return {
            bookings: [],
            cancelOpened: false,
            bookingId: null,
        };
    },
    methods: {
        openCancel(bookingId) {
            this.bookingId = bookingId;
        },
    },
});
app.mount("#app");
