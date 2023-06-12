import React, { useState, useContext } from "react";
import {
  Box,
  Card,
  DialogTitle,
  Button,
  useTheme,
  TextField,
  styled,
  MenuItem,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import client from "../../utils/clients";
import { FileContext } from "../../context/context";

import { tokens } from "../../theme";
import ModalDialog from "../../components/ModalDialog";
import { useGridApiOptionHandler } from "@mui/x-data-grid";

const StyledTextField = styled(TextField)(({ theme }) => ({
  margin: "15px 1rem",
  marginBottom: "10px",
  width: "90%",
  fontSize: "20px",
  "& .MuiInputBase-root": {
    height: "70px",
    fontSize: "20px",
    color: "#e0e0e0",
  },
  "& .MuiInputLabel-root": {
    fontSize: "19px",
    color: "#94e2cd",
  },
}));

const typeInfralist = [
  {
    value: "fin",
    label: "Financial",
  },
  {
    value: "man",
    label: "Manufacturing",
  },
  {
    value: "dev",
    label: "Devlopment",
  },
  {
    value: "npp",
    label: "NPP",
  },
];

const imgTypelist = [
  {
    value: "win",
    label: "Windows",
  },
  {
    value: "lin",
    label: "Linux",
  },
  {
    value: "mac",
    label: "Mac",
  },
];

const UserForm = (props) => {
  const navigate = useNavigate();

  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [typeOfInfra, setTypeOfInfra] = useState("");
  const [instances, setInstances] = useState("");
  const [routers, setRouters] = useState("");
  const [subnets, setSubnets] = useState("");
  const [imageType, setImageType] = useState("");

  const [result, setResult] = useState(false);
  const [open, setOpen] = useState(false);

  const { filename, setFilename, iac, setIac } = useContext(FileContext);

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    console.log(typeOfInfra, instances, routers, subnets, imageType);
    try {
      const res = await client.get(
        `/choice-iac?infraType=${typeOfInfra}&routeNum=${routers}&subnetNum=${subnets}&instanceNum=${instances}&imageType=${imageType}`
      );
      console.log(res);
      setFilename(res.data.fileName);
      setIac(res.data.code);
      setResult(res.data.result == "true" ? true : false);
      navigate("/viewcode");
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <Box
      component="form"
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
      onSubmit={handleFormSubmit}
    >
      <StyledTextField
        label="Type of Infra"
        select
        variant="filled"
        required
        value={typeOfInfra}
        onChange={(e) => setTypeOfInfra(e.target.value)}
      >
        {typeInfralist.map((option) => (
          <MenuItem key={option.value} value={option.value || ""}>
            {option.label}
          </MenuItem>
        ))}
      </StyledTextField>
      <StyledTextField
        label="Instances"
        variant="filled"
        required
        value={instances}
        onChange={(e) => setInstances(e.target.value)}
      />
      <StyledTextField
        label="Routers"
        variant="filled"
        required
        value={routers}
        onChange={(e) => setRouters(e.target.value)}
      />
      <StyledTextField
        label="Subnets"
        variant="filled"
        required
        value={subnets}
        onChange={(e) => setSubnets(e.target.value)}
      />
      <StyledTextField
        label="Image Type"
        select
        variant="filled"
        required
        value={imageType}
        onChange={(e) => setImageType(e.target.value)}
      >
        {imgTypelist.map((option) => (
          <MenuItem key={option.value} value={option.value || ""}>
            {option.label}
          </MenuItem>
        ))}
      </StyledTextField>
      <Box display="flex">
        <Button
          variant="outlined"
          color=""
          sx={{ margin: "1rem" }}
          color="error"
        >
          Cancel
        </Button>
        <Button variant="contained" type="submit" sx={{ margin: "1rem" }}>
          Generate
        </Button>
      </Box>
      {/* <ModalDialog
        open={open}
        handleClose={() => {
          setOpen((prev) => !prev);
        }}
      ></ModalDialog> */}
    </Box>
  );
};

export default UserForm;
