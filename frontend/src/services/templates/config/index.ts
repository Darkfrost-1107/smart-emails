import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:9800/api/",
})

export default api;