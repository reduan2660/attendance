<script setup>
import { RouterLink } from "vue-router";
import { useUserStore } from "@/stores/user";
import { onMounted } from "vue";

const { isLoggedIn, user, logUserOut } = useUserStore();
</script>

<template>
  <!-- <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
      </nav>
    </div>
  </header> -->

  <header>
    <div
      class="h-20 max-w-screen flex flex-row items-center justify-around shadow-md font-pathao text-lg"
    >
      <div><RouterLink to="/">CSEDU Attendance</RouterLink></div>

      <div>
        <div v-if="!isLoggedIn">
          <RouterLink to="/login">Login</RouterLink>
        </div>

        <div v-else class="flex flex-row gap-4 items-center">
          <div>{{ user.name }}</div>

          <div
            @click="logUserOut"
            class="px-2 py-1 border-red-300 border-2 rounded cursor-pointer"
          >
            Logout
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
