import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import ClassesView from "../views/ClassesView.vue";
import AttendanceView from "@/views/AttendanceView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/home",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/classes",
      name: "classes",
      component: ClassesView,
    },
    {
      path: "/attendance",
      name: "attendance",
      component: AttendanceView,
    },

    // Redirect to home view when url is not found
    {
      path: "/:pathMatch(.*)*",
      redirect: "/home",
    },
  ],
});

export default router;
