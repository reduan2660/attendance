<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter, useRoute } from "vue-router";

import Header from "../components/Header.vue";
import api from "../api";

// Toast
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const { isLoggedIn } = useUserStore();
const router = useRouter();
const route = useRoute();

const classes = ref([]);
const course_id = route.query.course_id;
const course_name = route.query.course_name;

const fetchClasses = () => {
  console.log("fetching classes");
  api
    .get(`/classes?course_id=${course_id}`, {
      headers: {
        token: localStorage.getItem("token"),
      },
    })

    .then((response) => {
      classes.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
};

const newClass = () => {
  api
    .post(
      `/newClass`,
      {
        course: course_id,
      },
      {
        headers: {
          token: localStorage.getItem("token"),
        },
      }
    )
    .then((response) => {
      console.log(response.data);
      toast.success("Class created");
      fetchClasses();
    })
    .catch((error) => {
      console.log(error);
      toast.error("Error creating class");
    });
};

const convertPythonTimestampToUTC6String = (pythonTimestamp) => {
  // Parse the Python timestamp
  const dateObject = new Date(pythonTimestamp);

  // Adjust for UTC+6
  dateObject.setHours(dateObject.getHours() + 6);

  // Format the date in DD-Mon-YY format
  const options = { day: "2-digit", month: "short", year: "2-digit" };
  const formattedString = dateObject.toLocaleDateString("en-US", options);

  return formattedString;
};

onMounted(() => {
  if (!isLoggedIn) {
    router.push("/login");
  }
  fetchClasses();
});
</script>

<template>
  <main>
    <Header />

    <div class="flex flex-col items-center my-6">
      <div class="flex flex-row justify-between items-center w-1/2">
        <div class="font-bold text-xl py-10">{{ course_name }}</div>
        <div
          class="px-2 py-1 rounded border-2 border-blue-300 cursor-pointer"
          @click="newClass"
        >
          Create new
        </div>
      </div>

      <!-- Loop thrugh all classes -->
      <div class="flex flex-row gap-20 flex-wrap mx-20">
        <div v-for="classs in classes" :key="classs.id">
          <div
            class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow"
          >
            <a href="#">
              <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
                {{ convertPythonTimestampToUTC6String(classs.class_time) }}
              </h5>
            </a>

            <p>
              Attendance -
              {{ parseFloat(classs.attendance_percentage).toFixed(2) }} %
            </p>

            <RouterLink
              :to="`/attendance?class_id=${classs.id}&course_name=${course_name}`"
              class="inline-flex items-center px-3 py-2 my-4 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300"
            >
              Take attendance
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
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
