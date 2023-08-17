import { useState } from "react";
import { useEffect } from "react";
import "./App.css";
import { WSS_URL } from "./constants";

function App() {
  // Websocket
  let ws = null;
  let [updateMessage, setUpdateMessage] = useState("");

  // Startup
  useEffect(() => {
    /* Connect to websocket */
    ws = new WebSocket(`${WSS_URL}/update`);
    ws.onopen = () => {
      console.log("connected");
      setUpdateMessage("connected");
    };
    ws.onmessage = (evt) => {
      // listen to data sent from the websocket server
      setUpdateMessage(evt.data);
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
    </>
  );
}

export default App;
