import React, { useState } from "react";
import { Box, useTheme } from "@mui/material";

import { tokens } from "../../theme";
import SelectCard from "../../components/SelectCard";
import ModalDialog from "../../components/ModalDialog";
import FileUpload from "../fileupload";
import UserForm from "../userform";

const Select = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [open, setOpen] = useState(false);
  const [openUser, setOpenUser] = useState(false);

  const handleOpen = () => {
    setOpen(true);
    console.log(open);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpenUser = () => {
    setOpenUser(true);
    console.log(openUser);
    console.log("test");
  };

  const handleCloseUser = () => {
    setOpenUser(false);
  };

  return (
    <div>
      <Box sx={{ height: "20vh" }} />
      <Box
      display="flex"
        sx={{
          height: "60vh",
          ml: "10%px",
          mr: "10%"
        }}
      >
        <img src='../../../assets/logo_text.png' alt="" style={{
          alignContent: "center",
          width: "25%",
          height: "50%",
          margin: "10%"
        }}/>
        <Box
          display="flex"
          sx={{
            width: "50%",
            float: "left",
            height: "100%",
            boxSizing: "border-box",
          }}
        >
          <SelectCard
            title="Upload IaC File"
            src="../../assets/upload.png"
            num="01"
            click={handleOpen}
          />
        </Box>
        <Box
          display="flex"
          textAlign="center"
          sx={{
            width: "50%",
            float: "right",
            height: "100%",
            boxSizing: "border-box",
          }}
        >
          <hr
            style={{
              height: "60vh",
              float: "left",
              background: `linear-gradient(transparent, ${colors.blueAccent[700]}, transparent)`,
              width: ".2vw",
              borderWidth: "0",
              color: "#000",
            }}
          />
          <SelectCard
            title="User Input"
            src="../../assets/input.png"
            num="02"
            click={handleOpenUser}
          />
          <ModalDialog
            open={openUser}
            handleClose={handleCloseUser}
            title="User Input Form"
            styled={"500px"}
          >
            <UserForm close={handleClose} />
          </ModalDialog>
          <ModalDialog
            open={open}
            handleClose={handleClose}
            title="File Upload"
            styled={"700px"}
          >
            <FileUpload />
          </ModalDialog>
        </Box>
      </Box>
    </div>
  );
};

export default Select;
