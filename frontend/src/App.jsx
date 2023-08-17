// React imports
import { useState } from "react";
import { useEffect } from "react";
import "./App.css";

// URL imports
import { WSS_URL } from "./constants";

// Toast imports
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  // Websocket
  let ws = null;
  let [updateMessage, setUpdateMessage] = useState("");

  // Toast
  const notify = (message) =>
    toast.success(message, {
      position: "top-center",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: false,
      draggable: true,
      progress: undefined,
      theme: "dark",
    });

  // Startup
  useEffect(() => {
    console.log("Startup");

    /* Connect to websocket */
    ws = new WebSocket(`${WSS_URL}/update`);
    ws.onopen = () => {
      console.log("connected");
      setUpdateMessage("connected");
    };
    ws.onmessage = (evt) => {
      // listen to data sent from the websocket server
      console.log(evt.data);
      setUpdateMessage(evt.data);
      notify(evt.data);
    };
    ws.onclose = () => {
      console.log("disconnected");
      setUpdateMessage("disconnected");
      // automatically try to reconnect on connection loss
    };
  }, []);

  return (
    <>
      <h1>{updateMessage}</h1>
      <ToastContainer
        position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss={false}
        draggable
        pauseOnHover={false}
        theme="dark"
      />
    </>
  );
}

export default App;
