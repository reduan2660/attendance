// React imports
import { useState } from "react";
import { useEffect } from "react";
import "./App.css";

// API & URL imports
import { WSS_URL } from "./constants";
import api from "./api";

// Toast imports
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// Antd imports
import { Table } from "antd";
import Column from "antd/es/table/Column";
import { Button, Modal } from "antd";

// React Router
import { Link } from "react-router-dom";

function App() {
  /// Modal
  const [isNewDeviceModalOpen, setIsNewDeviceModalOpen] = useState(false);

  // Websocket
  let ws = null;

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

  // Table Data
  const [attendanceData, setAttendanceData] = useState([]);

  const fetchAttendanceData = () => {
    api
      .get("/attendance")
      .then((res) => {
        console.log(res.data);
        setAttendanceData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // Startup
  useEffect(() => {
    console.log("Startup");

    /* Connect to websocket */
    ws = new WebSocket(`${WSS_URL}/update`);
    ws.onopen = () => {
      console.log("connected");
    };
    ws.onmessage = (evt) => {
      // listen to data sent from the websocket server
      console.log(evt.data);
      notify(evt.data);

      /* Fetch attendance data */
      fetchAttendanceData();
    };
    ws.onclose = () => {
      console.log("disconnected");
      // automatically try to reconnect on connection loss
    };

    /* Fetch attendance data */
    fetchAttendanceData();
  }, []);

  return (
    <div>
      <Link to="/link">
        <h1 style={{color: "white"}}>Attendance</h1>
      </Link>

      {/* Table */}
      <Table
        dataSource={attendanceData}
        rowKey="id"
        pagination={false}
        style={{ overflowX: "auto" }}
      >
        <Column
          title="Student"
          dataIndex="student_id"
          render={(student, record) => <p>{record.student.name}</p>}
        />
        <Column
          title="Course"
          dataIndex="course_id"
          render={(student, record) => <p>{record.course.name}</p>}
        />
        <Column title="Date" dataIndex="date"></Column>
        <Column title="Time" dataIndex="time"></Column>
      </Table>

      <a
        href="https://github.com/reduan2660/attendance"
        target="_blank"
        style={{
          position: "fixed",
          bottom: "10px",
          right: "10px",
          margin: "10px",

          color: "white",
          padding: "10px 10px",
          borderRadius: "5px",
          textDecoration: "none",
          border: "1px solid #aaaaaa",
        }}
      >
        Contribute
      </a>

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

export default App;
