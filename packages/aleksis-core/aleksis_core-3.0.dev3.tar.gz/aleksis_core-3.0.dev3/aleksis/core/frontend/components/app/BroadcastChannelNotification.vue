<template>
  <message-box :value="show" type="warning">
    {{ $t("alerts.page_cached") }}
  </message-box>
</template>

<script>
export default {
  name: "BroadcastChannelNotification",
  props: {
    channelName: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      show: false,
    };
  },
  created() {
    this.channel = new BroadcastChannel(this.channelName);
    this.channel.onmessage = (event) => {
      this.show = event.data === true;
    };
  },
  destroyed() {
    this.channel.close();
  },
};
</script>
