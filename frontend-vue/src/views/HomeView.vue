<script setup>
import { onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import Header from "../components/Header.vue";

const { isLoggedIn } = useUserStore();
const router = useRouter();

onMounted(() => {
  if (!isLoggedIn) {
    router.push("/login");
  }
});
</script>

<template>
  <main>
    <Header />
    <h1>Hello</h1>
  </main>
</template>
