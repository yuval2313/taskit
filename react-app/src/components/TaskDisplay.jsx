import React from "react";
import {
  Card,
  CardActions,
  CardContent,
  Typography,
  Button,
  Box,
} from "@mui/material";

const TaskDisplay = ({ id, title, body, statusDone, onEdit, onDeleteTask }) => {
  return (
    <Card sx={{ opacity: statusDone ? 0.8 : 1 }}>
      <CardContent sx={{ opacity: statusDone ? 0.5 : 1 }}>
        <Typography
          variant="h5"
          component="div"
          sx={{
            marginBottom: 2,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {title ? title : "Untitled"}
        </Typography>
        <Typography
          color="text.secondary"
          sx={{
            height: "204px",
            overflowY: "auto", // scrollbar when the content exceeds the height
            whiteSpace: "pre-line", // preserve newline
          }}
        >
          {body ? body : "..."}
        </Typography>
      </CardContent>
      <CardActions
        sx={{
          justifyContent: "space-between",
          padding: 2,
        }}
      >
        <Box sx={{ display: "flex", gap: 1.5 }}>
          <Button variant="outlined" onClick={onEdit}>
            Edit
          </Button>
          <Button
            variant="outlined"
            color="error"
            onClick={() => onDeleteTask(id)}
          >
            Delete
          </Button>
        </Box>
        <Typography variant="h6" sx={{ marginRight: 2 }}>
          {statusDone ? "Done!" : ""}
        </Typography>
      </CardActions>
    </Card>
  );
};

export default TaskDisplay;
