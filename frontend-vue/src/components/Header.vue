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
    <div class="h-20 max-w-screen flex flex-row items-center justify-around">
      <div><RouterLink to="/">Attendance</RouterLink></div>

      <div>
        <div v-if="!isLoggedIn">
          <RouterLink to="/login">Login</RouterLink>
        </div>

        <div v-else class="flex flex-row">
          <div>{{ user.name }}</div>
          |
          <div @click="logUserOut">Logout</div>
        </div>
      </div>
    </div>
  </header>
</template>
