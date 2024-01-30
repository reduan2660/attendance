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

onMounted(() => {
  if (!isLoggedIn) {
    router.push("/login");
  }
  fetchattendances();
});
</script>

<template>
  <main>
    <Header />

    <div class="flex flex-col items-center my-6">
      <div class="font-bold text-xl py-10">{{ course_name }}</div>

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
                <Tag class="p-tag-success">Present</Tag>
              </div>
              <div v-else>
                <Tag class="p-tag-danger">Absent</Tag>
              </div>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </main>
</template>
