<template>
  <div
    class="d-flex justify-center align-center flex-column text-center"
    id="wrapper"
  >
    <h1 class="text-h2">{{ $t(shortErrorMessageKey) }}</h1>
    <div>{{ $t(longErrorMessageKey) }}</div>
    <v-btn color="secondary" :to="{ name: 'dashboard' }">
      <v-icon left>mdi-home-outline</v-icon>
      {{ $t("network_errors.back_to_start") }}
    </v-btn>
  </div>
</template>

<script>
export default {
  name: "ErrorPage",
  props: {
    shortErrorMessageKey: {
      type: String,
      required: true,
    },
    longErrorMessageKey: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
#wrapper {
  min-height: 70vh;
  gap: 1em;
}
</style>
