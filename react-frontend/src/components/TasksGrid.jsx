import React from "react";
import Task from "components/Task";
import { Grid, Box } from "@mui/material";

const TasksGrid = ({ tasks, onUpdateTask, onDeleteTask }) => {
  return (
    <div style={{ padding: "16px" }}>
      <Grid container spacing={2}>
        {tasks.map((task, index) => (
          <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
            <Box m={1}>
              <Task
                {...task}
                onUpdateTask={onUpdateTask}
                onDeleteTask={onDeleteTask}
              />
            </Box>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default TasksGrid;
