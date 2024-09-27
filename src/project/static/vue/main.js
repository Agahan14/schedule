createApp({
    components: {
        CreateEvent,
        CreateAvailability
    },
    data() {
        return {
            createEventOpened: false,
            createAvailabilityOpened: false,
            availabilityName: "",
            isDefault: false,
            workSchedule: [],
            availabilityId: 2
        };

    },
    methods: {
        createAvailability() {
            this.createAvailabilityOpened = true;
        },
        closeAvailability() {
            this.createAvailabilityOpened = false;
        },
        async fetchAvailability(id) {
            try {
                const response = await fetch(`/availability/${id}`);

                console.log(response.data)
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const availabilityData = await response.json();
                console.log(availabilityData)

                this.availabilityName = availabilityData.name;
                this.isDefault = availabilityData.is_default;
                this.workSchedule = availabilityData.work_schedule.map(day => ({
                    day_of_week: day.day_of_week,
                    time_from: day.time_from,
                    time_to: day.time_to,
                    is_active: day.is_active
                }));
            } catch (error) {
                console.error("Error fetching availability:", error);
            }
        },
        async saveData(availabilityId) {
                console.log(this.$ref.name.value)
            console.log("here")
            // console.log(defaultWorkSchedule);
            // try {
            //     const response = await fetch(`/availability/${availabilityId}`, {
            //         method: "POST",
            //         headers: {
            //             "Content-Type": "application/json"
            //         },
            //         body: JSON.stringify(defaultWorkSchedule)
            //     });
            //
            //     if (!response.ok) {
            //         throw new Error("Failed to save data");
            //     }
            //
            //     const result = await response.json();
            //     console.log("Successfully saved data:", result);
            //
            // } catch (error) {
            //     console.error("Error saving data:", error);
            // }

        }
    },
}).mount("#app");
