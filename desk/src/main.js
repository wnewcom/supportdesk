import { createApp } from "vue";
import {
  Badge,
  Button,
  FormControl,
  frappeRequest,
  FrappeUI,
  setConfig,
  TextInput,
  toast,
} from "frappe-ui";
import App from "./App.vue";
import "./index.css";
import { router } from "./router";

setConfig("resourceFetcher", frappeRequest);
setConfig("fallbackErrorHandler", (error) => {
  const msg = error.exc_type
    ? (error.messages || error.message || []).join(", ")
    : error.message;
  toast.error(msg);
});

const app = createApp(App);
app.use(FrappeUI);
app.use(router);
app.mount("#app");
