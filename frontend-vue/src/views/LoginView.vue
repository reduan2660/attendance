<script setup>
import { onMounted, ref, reactive } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

import api from "@/api";

// Toast
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const { isLoggedIn, user, logUserIn } = useUserStore();
const router = useRouter();

const email = ref("");
const password = ref("");

const login = () => {
  api
    .post("/login/", { email: email.value, password: password.value })
    .then((res) => {
      localStorage.setItem("token", res.data.token);
      api
        .get("/me", {
          headers: {
            token: res.data.token,
          },
        })
        .then((response) => {
          const user = response.data;
          logUserIn(user);
          router.push("/home");
        })
        .catch((error) => {
          console.log(error);
          toast.error("Invalid Credentials");
        });
    })
    .catch((err) => {
      console.log(err);
      toast.error("Invalid Credentials");
    });
};

onMounted(() => {
  if (isLoggedIn) {
    router.push("/home");
  }
});
</script>

<template>
  <section class="bg-gray-5">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0"
    >
      <a
        href="#"
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900"
      >
        <img class="w-8 h-8 mr-2" src="@/images/csedu.png" alt="logo" />
        Attendance
      </a>
      <div class="w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl"
          >
            Sign in to your account
          </h1>
          <form class="space-y-4 md:space-y-6" action="#">
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Your email</label
              >
              <input
                type="email"
                name="email"
                id="email"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                placeholder="name@du.ac.bd"
                required
                v-model="email"
              />
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900"
                >Password</label
              >
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
                required
                v-model="password"
              />
            </div>
            <button
              type="button"
              class="w-full text-white bg-gray-600 bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
              @click="login"
            >
              Sign in
            </button>
            <!-- <p class="text-sm font-light text-gray-500">
              Don’t have an account yet?
              <a href="#" class="font-medium text-primary-600 hover:underline"
                >Sign up</a
              >
            </p> -->
          </form>
        </div>
      </div>
    </div>
  </section>
</template>
