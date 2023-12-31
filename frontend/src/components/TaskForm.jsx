import React, { useState } from "react";
import {
  Card,
  CardActions,
  CardContent,
  Typography,
  TextField,
  Button,
  Checkbox,
  Box,
  Divider,
} from "@mui/material";

const TaskForm = ({
  id = "",
  title = "",
  body = "",
  statusDone = false,
  onSave,
  onCancel,
}) => {
  const [editedTitle, setEditedTitle] = useState(title);
  const [editedBody, setEditedBody] = useState(body);
  const [editedStatusDone, setEditedStatusDone] = useState(statusDone);

  const handleSaveClick = () => {
    onSave({
      id,
      title: editedTitle,
      body: editedBody,
      statusDone: editedStatusDone,
    });
    onCancel();
  };

  return (
    <Card>
      <CardContent>
        <TextField
          label="Title"
          variant="outlined"
          fullWidth
          value={editedTitle}
          onChange={(e) => setEditedTitle(e.target.value)}
          sx={{ marginBottom: 2 }}
        />
        <TextField
          label="Body"
          variant="outlined"
          multiline
          rows={4}
          fullWidth
          value={editedBody}
          onChange={(e) => setEditedBody(e.target.value)}
          sx={{ marginBottom: 2 }}
        />
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <Typography style={{ paddingLeft: "5px" }}>
            Mark Completed -
          </Typography>
          <Checkbox
            size="small"
            color="primary"
            checked={editedStatusDone}
            onChange={(e) => setEditedStatusDone(e.target.checked)}
            sx={{ alignSelf: "flex-end" }}
          />
        </Box>
      </CardContent>
      <Divider />
      <CardActions sx={{ justifyContent: "space-between", padding: 2 }}>
        <Button onClick={handleSaveClick}>Save</Button>
        <Button onClick={onCancel}>Cancel</Button>
      </CardActions>
    </Card>
  );
};

export default TaskForm;
