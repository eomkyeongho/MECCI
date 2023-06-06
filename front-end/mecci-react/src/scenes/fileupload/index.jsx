import { useRef, useState, useContext } from "react";
import {
  Box,
  useTheme,
  theme,
  styled,
  TextField,
  MenuItem,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import CloudDownloadIcon from "@mui/icons-material/CloudDownload";
import PostAddIcon from "@mui/icons-material/PostAdd";
import CheckIcon from "@mui/icons-material/Check";
import "./fileupload.css";
import { tokens } from "../../theme";
import { UploadFile } from "@mui/icons-material";
import axios from "axios";
import client from "../../utils/clients";
import ModalDialog from "../../components/ModalDialog";
import { FileContext } from "../../context/context";

const StyledTextField = styled(TextField)(({ theme }) => ({
  margin: "1rem",
  width: "90%",
  fontSize: "20px",
  "& .MuiInputBase-root": {
    height: "75px",
    fontSize: "25px",
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

const FileUpload = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const formRef = useRef();
  const fileInputRef = useRef();
  const progressAreaRef = useRef();
  const uploadedAreaRef = useRef();

  const [open, setOpen] = useState(false);
  const { filename, setFilename, iac, setIac } = useContext(FileContext);
  const [selected, setSeleted] = useState("");

  const navigate = useNavigate();

  const formClickHandler = () => {
    const fileCurrent = fileInputRef.current;

    fileCurrent.click();

    fileCurrent.onchange = ({ target }) => {
      let file = target.files[0];
      setOpen(true);
      setFilename(file);
    };
  };

  const uploadFile = async (val) => {
    const formData = new FormData(formRef.current);

    formData.append("file", filename);
    formData.append("name", filename.name);
    formData.append("industry", val);

    for (let key of formData.keys()) {
      console.log(key);
    }

    /* value 확인하기 */
    for (let value of formData.values()) {
      console.log(value);
    }

    try {
      const res = await client.post("/upload-tf", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const result = {
        status: res.status + "-" + res.statusText,
        headers: res.headers,
        data: res.data,
      };

      setFilename(res.data.fileName);
      if (!res.data.debug) {
        setIac(res.data.code);
        navigate("/viewcode");
      } else {
        setOpen(false);
      }
      console.log(res);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <div className="wrapper">
        <form ref={formRef} onClick={formClickHandler} action="#">
          <input ref={fileInputRef} type="file" className="file-input" hidden />
          <CloudDownloadIcon
            sx={{
              fontSize: "80px",
            }}
          />
          <p>Browse file to Upload</p>
        </form>
        <ModalDialog
          open={open}
          title="Type of Infra"
          handleClose={() => setOpen(false)}
        >
          <StyledTextField
            label="Select Infra Type"
            select
            variant="filled"
            value={selected}
            required
            onChange={(e) => {
              setSeleted(e.target.value);
              uploadFile(e.target.value);
            }}
          >
            {typeInfralist.map((option) => (
              <MenuItem key={option.value} value={option.value || ""}>
                {option.label}
              </MenuItem>
            ))}
          </StyledTextField>
        </ModalDialog>
      </div>
    </>
  );
};

export default FileUpload;
