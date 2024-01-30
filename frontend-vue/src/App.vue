<script setup>
import { onBeforeMount, onMounted } from "vue";

import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import api from "./api";
const { isLoggedIn, user, logUserIn, logUserOut } = useUserStore();
const router = useRouter();

onBeforeMount(() => {
  // check for token in local storage
  // if token exists, fetch user
  // if user exists, log user in
  // if user does not exist, log user out

  const token = localStorage.getItem("token");
  if (token) {
    api
      .get("/me", {
        headers: {
          token: token,
        },
      })
      .then((response) => {
        const user = response.data;
        logUserIn(user);

        router.push("/home");
      })
      .catch((error) => {
        console.log(error);
        logUserOut();
      });
  } else {
    router.push("/login");
  }
});
</script>

<template>
  <!-- <Header /> -->

  <RouterView />
</template>
