<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

import Header from "../components/Header.vue";
import api from "../api";

const { isLoggedIn } = useUserStore();
const router = useRouter();

const courses = ref([]);

const fetchCourses = () => {
  console.log("fetching courses");
  api
    .get("/courses", {
      headers: {
        token: localStorage.getItem("token"),
      },
    })

    .then((response) => {
      courses.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  if (!isLoggedIn) {
    router.push("/login");
  }

  fetchCourses();
});
</script>

<template>
  <main>
    <Header />

    <div class="flex flex-col items-center my-6">
      <div class="font-bold text-xl py-10">My courses</div>

      <!-- Loop thrugh all courses -->
      <div v-for="course in courses" :key="course.id">
        <div
          class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow"
        >
          <a href="#">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
              {{ course.code }}
            </h5>
          </a>

          <p>{{ course.name }} - {{ course.year }}</p>

          <a
            href="#"
            class="inline-flex items-center px-3 py-2 my-4 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300"
          >
            Classes
            <svg
              class="rtl:rotate-180 w-3.5 h-3.5 ms-2"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 10"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M1 5h12m0 0L9 1m4 4L9 9"
              />
            </svg>
          </a>
        </div>
      </div>
    </div>
  </main>
</template>
