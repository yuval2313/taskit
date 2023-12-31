import React from "react";
import TaskForm from "components/TaskForm";

const NewTaskForm = ({ onSave, onCancel }) => {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.5)", // Semi-transparent black background
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 999, // Ensure the overlay is above other content
      }}
    >
      <TaskForm onSave={onSave} onCancel={onCancel} />
    </div>
  );
};

export default NewTaskForm;
