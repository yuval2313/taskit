import React from "react";

import { TextField, Button, Box } from "@mui/material";

function TasksHead({ searchQuery, onSearch, onAddTask }) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        margin: "auto",
        marginBottom: 2,
        padding: "0 1rem",
        maxWidth: "600px",
      }}
    >
      <Box sx={{ display: "flex", gap: 2, alignItems: "center", flex: 1 }}>
        <TextField
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => onSearch(e.target.value)}
          sx={{ flex: 1, background: "#fff" }}
        />
        <Button variant="contained" onClick={onAddTask}>
          Add Task
        </Button>
      </Box>
    </Box>
  );
}

export default TasksHead;
