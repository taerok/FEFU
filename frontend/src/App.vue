<template>
  <div id="app">
    <v-app id="inspire" style="background: #fcfcfc">
      <core-header />
      <v-main>
        <router-view />
      </v-main>
      <core-footer />
      <chat-button v-if="isLoggedIn" />
    </v-app>
  </div>
</template>

<script>
import ChatButton from "@/components/Chat/ChatButton.vue";
import CoreFooter from "@/components/core/Footer";
import CoreHeader from "@/components/core/Header";
import { mapGetters } from "vuex";

export default {
  components: {
    ChatButton,
    CoreFooter,
    CoreHeader,
  },
  computed: {
    ...mapGetters("accounts", ["isLoggedIn"]),
  },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Nunito:wght@400;600;700;800;900&display=swap");
@font-face {
  font-family: "NanumSquareRound";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/NanumSquareRound.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: "NanumBarunpen";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/NanumBarunpen.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}

:root {
  --primary-color: #37cdc2;
  --white-color: #fcfcfc;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
