const { defineComponent, createApp } = Vue;

const TestComponent = defineComponent({
  template: "#test-template",
  methods: {
    closeTest() {
      this.$emit("close-test");
    },
  },
});
