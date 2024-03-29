<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter, useRoute } from "vue-router";

import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Tag from "primevue/tag";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Dropdown from "primevue/dropdown";
import InputText from "primevue/inputtext";
import Checkbox from "primevue/checkbox";
import Paginator from "primevue/paginator";

import Header from "../components/Header.vue";
import api from "../api";
import { WSS_URL } from "../constants";

// Toast
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const { isLoggedIn } = useUserStore();
const router = useRouter();
const route = useRoute();

const attendances = ref([]);
const course_class_id = route.query.class_id;
const course_name = route.query.course_name;

const fetchattendances = () => {
  console.log("fetching attendances");
  api
    .get(`/attendance?course_class_id=${course_class_id}`, {
      headers: {
        token: localStorage.getItem("token"),
      },
    })

    .then((response) => {
      attendances.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
};

const updateAttendance = (attendance_id, is_present) => {
  api
    .put(
      `/attendance?attendance_id=${attendance_id}&is_present=${is_present}`,
      {},
      {
        headers: {
          token: localStorage.getItem("token"),
        },
      }
    )
    .then((response) => {
      console.log(response.data);
      toast.success("Attendance updated");
      fetchattendances();
    })
    .catch((error) => {
      console.log(error);
      toast.error("Error updating attendance");
    });
};

const linkDevice = () => {
  api
    .get(`/linkDevice?course_class_id=${course_class_id}&device_id=1`, {
      headers: {
        token: localStorage.getItem("token"),
      },
    })
    .then((response) => {
      console.log(response.data);
      toast.success("Device linked");
      fetchattendances();
    })
    .catch((error) => {
      console.log(error);
      toast.error("Error linking device");
    });
};

onMounted(() => {
  if (!isLoggedIn) {
    router.push("/login");
  }
  // fetchattendances();

  const ws = new WebSocket(`${WSS_URL}/update`);
  ws.onopen = () => {
    console.log("connected");
  };
  ws.onmessage = (evt) => {
    // listen to data sent from the websocket server
    console.log(evt.data);
    toast.success(evt.data);

    /* Fetch attendance data */
    fetchattendances();
  };
  ws.onclose = () => {
    console.log("disconnected");
    // automatically try to reconnect on connection loss
  };

  /* Fetch attendance data */
  fetchattendances();
});
</script>

<template>
  <main>
    <Header />

    <div class="flex flex-col items-center my-6">
      <div class="w-1/2 flex flex-row justify-between items-center">
        <div class="font-bold text-xl py-10">{{ course_name }}</div>

        <div
          @click="linkDevice"
          class="cursor-pointer py-1 px-2 shadow rounded border-2 border-gray-400"
        >
          Link Device
        </div>
      </div>

      <div class="card">
        <DataTable
          :value="attendances"
          class="w-full"
          tableStyle="min-width: 50rem; font-family: 'Titillium Web', sans-serif;"
          :paginator="true"
          :rows="20"
          :rowsPerPageOptions="[20, 100]"
          sortField="student.roll"
          sortOrder="1"
        >
          <Column field="student.name" header="name"></Column>
          <Column field="student.roll" header="Roll" sortable></Column>
          <Column field="is_present" header="Status">
            <template #body="slotProps">
              <div v-if="slotProps.data.is_present">
                <Tag
                  class="p-tag-success cursor-pointer"
                  @click="() => updateAttendance(slotProps.data.id, false)"
                  >Present</Tag
                >
              </div>
              <div v-else>
                <Tag
                  @click="() => updateAttendance(slotProps.data.id, true)"
                  class="p-tag-danger cursor-pointer"
                  >Absent</Tag
                >
              </div>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </main>
</template>
