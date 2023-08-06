<!--
  Base component to load legacy views from Django.

  It loads the legacy view into an iframe and attaches some utility
  code to it. The legacy application and the new Vue application can
  communicate with each other through a message channel.

  This helps during the migration from the pure SSR Django application
  in AlekSIS 2.x to the pure Vue and GraphQL based application.
  It will be removed once legacy view get unsupported.
-->

<template>
  <iframe
    :src="'/django' + $route.path + queryString"
    :height="iFrameHeight + 'px'"
    class="iframe-fullsize"
    @load="load"
    ref="contentIFrame"
  ></iframe>
</template>

<script>
export default {
  data: function () {
    return {
      iFrameHeight: 0,
    };
  },
  computed: {
    queryString() {
      let qs = [];
      for (const [param, value] of Object.entries(this.$route.query)) {
        qs.push(`${param}=${encodeURIComponent(value)}`);
      }
      return "?" + qs.join("&");
    },
  },
  methods: {
    /** Receives a message from the legacy app inside the iframe */
    receiveMessage(event) {
      if (event.data.height) {
        // The iframe communicated us its render height
        //  Set iframe to full height to prevent an inner scroll bar
        this.iFrameHeight = event.data.height;
        this.$root.contentLoading = false;
      }
    },
    /** Handle iframe data after inner page loaded */
    load() {
      // Write new location of iframe back to Vue Router
      const location = this.$refs.contentIFrame.contentWindow.location;
      const url = new URL(location);
      const path = url.pathname.replace(/^\/django/, "");
      const routePath =
        path.charAt(path.length - 1) === "/" &&
        this.$route.path.charAt(path.length - 1) !== "/"
          ? this.$route.path + "/"
          : this.$route.path;
      if (path !== routePath) {
        this.$router.push(path);
      }

      // Show loader if iframe starts to change its content, even if the $route stays the same
      this.$refs.contentIFrame.contentWindow.onpagehide = () => {
        this.$root.contentLoading = true;
      };

      // Write title of iframe to SPA window
      const title = this.$refs.contentIFrame.contentWindow.document.title;
      this.$root.$setPageTitle(title);
    },
  },
  mounted() {
    // Subscribe to message channel to receive height from iframe
    this.safeAddEventListener(window, "message", this.receiveMessage);
  },
  watch: {
    $route() {
      // Show loading animation once route changes
      this.$root.contentLoading = true;
    },
  },
  name: "LegacyBaseTemplate",
};
</script>

<style scoped>
.iframe-fullsize {
  border: 0;
  width: calc(100% + 24px);
  margin: -12px;
}
</style>
