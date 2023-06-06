import { Dialog, Box, DialogTitle } from "@mui/material";
import React from "react";

const ModalDialog = (props) => {
  const { open, handleClose, children, title, styled } = props;
  return (
    <Dialog open={open} onClose={handleClose}>
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        height="100%"
      >
        <Box
          sx={{
            width: `${styled}`,
            padding: "30px 40px",
            backgroundColor: "#1F2A40",
          }}
        >
          <DialogTitle
            sx={{
              color: "#fff",
              fontSize: "40px",
              fontWeight: "600",
              textAlign: "center",
            }}
          >
            {title}
          </DialogTitle>
          {children}
        </Box>
      </Box>
    </Dialog>
  );
};

export default ModalDialog;
