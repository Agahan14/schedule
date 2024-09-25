export default {
    data() {
        return {
            currentDate: new Date(),
            is24HourFormat: false,
            selectedDate: null,
            selectedTime: null,
            event: {
                title: "Sample Event",
                duration: "30",
                time_type: { value: "minutes" },
            },
        };
    },
    computed: {
        monthYearText() {
            return this.currentDate.toLocaleString("default", { month: "long", year: "numeric" });
        },
        calendarDays() {
            const year = this.currentDate.getFullYear();
            const month = this.currentDate.getMonth();
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const days = [];

            for (let i = 0; i < firstDay.getDay(); i++) {
                days.push({ day: ".", dateString: null });
            }

            for (let day = 1; day <= lastDay.getDate(); day++) {
                const date = new Date(year, month, day);
                const dateString = this.formatDate(date);
                days.push({
                    day,
                    dateString,
                    isToday: this.isToday(date),
                });
            }

            return days;
        },
        timeSlots() {
            const slots = [];
            const format = this.is24HourFormat ? "2-digit" : "numeric";
            const options = { hour: format, minute: "2-digit", hour12: !this.is24HourFormat };

            for (let hour = 0; hour < 24; hour++) {
                const time = new Date(2024, 0, 1, hour, 0);
                slots.push(time.toLocaleTimeString("en-US", options));
            }

            return slots;
        },
    },
    methods: {
        formatDate(date) {
            return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
        },
        isToday(date) {
            const today = new Date();
            return (
                date.getDate() === today.getDate() &&
                date.getMonth() === today.getMonth() &&
                date.getFullYear() === today.getFullYear()
            );
        },
        selectDate(dateString) {
            if (dateString) {
                this.selectedDate = dateString;
            }
        },
        selectTime(timeString) {
            this.selectedTime = timeString;
        },
        prevMonth() {
            this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1, 1);
        },
        nextMonth() {
            this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 1);
        },
        toggleView(is24Hour) {
            this.is24HourFormat = is24Hour;
        },
    },
};
