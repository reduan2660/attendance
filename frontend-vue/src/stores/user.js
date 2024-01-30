import { ref, computed } from "vue";
import { defineStore } from "pinia";

import api from "../api";

export const useUserStore = defineStore("user", () => {
  // const count = ref(0)
  // const doubleCount = computed(() => count.value * 2)
  // function increment() {
  //   count.value++
  // }

  // return { count, doubleCount, increment }

  const isLoggedIn = ref(false);
  const user = ref(null);

  function logUserIn(_user) {
    user.value = _user;
    isLoggedIn.value = true;

    console.log("Got user", user);
  }

  function logUserOut() {
    localStorage.removeItem("token");
    isLoggedIn.value = false;
    user.value = null;
  }

  return { isLoggedIn, user, logUserIn, logUserOut };
});
