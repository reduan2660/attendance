import axios from "axios";
import { BACKEND_URL } from "./constants";

export default axios.create({
  baseURL: BACKEND_URL,
  timeout: 6000,
  // withCredentials: true,
});
