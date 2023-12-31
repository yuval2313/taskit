import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";

const NavBar = () => {
  return (
    <AppBar position="static">
      <Toolbar
        style={{ display: "flex", justifyContent: "center", height: "80px" }}
      >
        <Typography
          variant="h3"
          style={{ fontWeight: "bold", textShadow: "0 0 4px #fff" }}
        >
          Task-it
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
