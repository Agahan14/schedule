createApp({
    components: {
        CreateEvent,
        CreateAvailability
    },
    data() {
        return {
            createEventOpened: false,
            createAvailabilityOpened: false
        };

    },
    methods: {
        createAvailability() {
            this.createAvailabilityOpened = true;
        },
        closeAvailability() {
            this.createAvailabilityOpened = false;
        },

        async saveData(availabilityId) {
            const availabilityName = this.$refs.availabilityName.value;
            const isDefault = this.$refs.defaultCheckbox.checked;
            const inputsContainer = this.$refs.inputs;
            const inputs = inputsContainer.querySelectorAll("input");
            const scheduleData = [];
            let schedule = {};
            inputs.forEach(input => {
                const scheduleId = input.dataset.scheduleId; // Retrieve the schedule ID from data attribute
                const inputName = input.name; // Get the name attribute to identify the type of input

                if (!schedule[scheduleId]) {
                    // Initialize a new schedule entry if not already created
                    schedule[scheduleId] = {
                        day_of_week: "",
                        time_from: "",
                        time_to: "",
                        is_active: false
                    };
                }

                // Set the value based on the input name
                if (inputName === "day_of_week") {
                    schedule[scheduleId].day_of_week = input.value;
                } else if (inputName === "time_from") {
                    schedule[scheduleId].time_from = input.value;
                } else if (inputName === "time_to") {
                    schedule[scheduleId].time_to = input.value;
                } else if (inputName === "active") {
                    schedule[scheduleId].is_active = input.checked;
                }
            });

            // Convert the object to an array
            Object.keys(schedule).forEach(key => {
                scheduleData.push(schedule[key]);
            });

            const data_structure = {
                name: availabilityName,
                is_default: isDefault,
                work_schedule: scheduleData
            };

            console.log(data_structure);
            try {
                const response = await fetch(`/availability/${availabilityId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data_structure) // Convert data structure to JSON
                });

                if (!response.ok) {
                    throw new Error("Failed to save data");
                }

                const result = await response.json();
                console.log("Successfully saved data:", result);
                window.location.href = `/availability/${availabilityId}`;

            } catch (error) {
                console.error("Error saving data:", error);
            }

        }

    }

}).mount("#app");
