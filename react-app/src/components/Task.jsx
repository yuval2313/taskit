import React, { useState } from "react";
import TaskDisplay from "components/TaskDisplay";
import TaskForm from "components/TaskForm";

const Task = ({ id, title, body, statusDone, onUpdateTask, onDeleteTask }) => {
  const [editing, setEditing] = useState(false);

  const handleEdit = () => {
    setEditing(true);
  };

  const handleCancelEdit = () => {
    setEditing(false);
  };

  return editing ? (
    <TaskForm
      id={id}
      title={title}
      body={body}
      statusDone={statusDone}
      onSave={onUpdateTask}
      onCancel={handleCancelEdit}
    />
  ) : (
    <TaskDisplay
      id={id}
      title={title}
      body={body}
      statusDone={statusDone}
      onDeleteTask={onDeleteTask}
      onEdit={handleEdit}
    />
  );
};

export default Task;
