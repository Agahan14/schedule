const { defineComponent, createApp } = Vue;

const CreateEvent = defineComponent({
    template: "#create-event-template"
});

const CreateAvailability = defineComponent({
    template: "#create-availability-template",
    data() {
        return {
            name: ""
        };
    },

    methods: {
        async submitAvailability() {
            try {
                const response = await fetch("/create_availability", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ name: this.name })
                });

                if (response.redirected) {
                    window.location.href = response.url;
                }

            } catch (error) {
                console.error("There was a problem with the fetch operation:", error);
            }
        }
    }
});