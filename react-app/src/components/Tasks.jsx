import React, { useState, useEffect } from "react";
import { Divider } from "@mui/material";
import TasksHead from "components/TasksHead";
import TasksGrid from "components/TasksGrid";
import NewTaskForm from "components/NewTaskForm";
import * as tasksService from "services/tasksService";

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddingTask, setIsAddingTask] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const data = await tasksService.getTasks();
      setTasks(data);
    } catch (error) {
      if (error.response && error.response.status === 404)
        console.warn("Tasks not found:", error);
      else console.error("Error fetching tasks:", error);
    }
  };

  const handleCreateTask = async (task) => {
    try {
      const data = await tasksService.saveTask(task);
      setTasks((prevTasks) => [data, ...prevTasks]);
    } catch (error) {
      console.error("Error creating task:", error);
      alert("Oops! Something went wrong. Please try again.");
    }
  };

  const handleUpdateTask = async (task) => {
    const { id: taskId, title, body, statusDone } = task;
    const originalState = [...tasks];

    // Update the local state
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, title, body, statusDone } : task
      )
    );

    try {
      // Update task on the backend
      await tasksService.saveTask(task);
    } catch (error) {
      console.error("Error updating task:", error);
      // If unsuccessfully revert back the state
      setTasks(originalState);
      alert("Oops! Something went wrong. Please try again.");
    }
  };

  const handleDeleteTask = async (taskId) => {
    const originalState = [...tasks];

    // Update the local state
    setTasks(tasks.filter((task) => task.id !== taskId));

    try {
      // Delete task on the backend
      await tasksService.deleteTask(taskId);
    } catch (error) {
      console.error("Error deleting task:", error);
      // If unsuccessfully revert back the state
      setTasks(originalState);
      alert("Oops! Something went wrong. Please try again.");
    }
  };

  const handleAddTask = () => {
    setSearchQuery("");
    setIsAddingTask(true);
  };

  const handleCancelAddTask = () => {
    setIsAddingTask(false);
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  function getFilteredTasks() {
    const filteredTasks = searchQuery
      ? tasks.filter(
          (t) =>
            t.title.match(new RegExp(`${searchQuery}`, "i")) ||
            t.body.match(new RegExp(`${searchQuery}`, "i"))
        )
      : tasks;
    return filteredTasks;
  }

  return (
    <div style={{ padding: "16px" }}>
      <TasksHead
        onAddTask={handleAddTask}
        onSearch={handleSearch}
        searchQuery={searchQuery}
      />
      <Divider />
      <TasksGrid
        tasks={getFilteredTasks()}
        onUpdateTask={handleUpdateTask}
        onDeleteTask={handleDeleteTask}
      />
      {isAddingTask && (
        <NewTaskForm onSave={handleCreateTask} onCancel={handleCancelAddTask} />
      )}
    </div>
  );
};

export default Tasks;
