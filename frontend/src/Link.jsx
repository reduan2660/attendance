// API & URL imports
import { WSS_URL } from "./constants";
import api from "./api";

// Antd
import { Input, Select, Space } from "antd";

// Toast imports
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { ApiOutlined, BookOutlined } from "@ant-design/icons";
import { useState } from "react";

function Link() {
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

  const linkDevice = (e) => {
    e.preventDefault();

    api
      .post("/link", {
        course: selectedCourse,
        device: selectedDevice,
        password: password,
      })
      .then((res) => {
        notify("Linked");
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const handleChange = (value) => {
    console.log(`selected ${value}`);
  };

  const [selectedCourse, setSelectedCourse] = useState(1);
  const [selectedDevice, setSelectedDevice] = useState(1);
  const [password, setPassword] = useState("");

  return (
    <div>
      <form onSubmit={linkDevice}>
        <Space style={{ marginBottom: "1rem" }}>
          <Select
            defaultValue="1"
            style={{ width: 300 }}
            onChange={(value) => setSelectedCourse(value)}
            options={[
              { value: "1", label: "Operating System" },
              { value: "2", label: "Lab: Operating System" },
            ]}
          />
          <Select
            defaultValue="1"
            style={{ width: 300 }}
            onChange={(value) => setSelectedDevice(value)}
            options={[{ value: "1", label: "Pilot", selected: true }]}
          />
        </Space>

        <Input
        type="password"
          size="large"
          name="course"
          placeholder="Password"
          onChange={(value) => setPassword(value.target.value)}
          style={{ marginBottom: "1rem"}}
        />

        <Input type="submit" value="Link" />
      </form>

      {/* Toast */}
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
    </div>
  );
}

export default Link;
