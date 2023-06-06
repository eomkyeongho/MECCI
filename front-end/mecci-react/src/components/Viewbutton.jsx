import { Button, useTheme, Box, Typography } from "@mui/material";
import { LoadingButton } from '@mui/lab';
import { tokens } from "../theme";

const Viewbutton = ({ title, color, col, row, width, click, disabled, loading }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box gridColumn={col} gridRow={row} display="flex" justifyContent="center"
      sx={{
        width: "100%",
      }}>
      <LoadingButton
        variant="contained"
        onClick={click}
        sx={{
          backgroundColor: colors.blueAccent[800],
          boxShadow: "15",
          color: `colors.${color}`,
          fontSize: "18px",
          fontWeight: "bold",
          justifyContent: "center",
          alignItems: "center",
          width: { width },
          height: "80%",
          maxWidth: "150px",
          borderRadius: "20px"
        }}
        disabled={disabled}
        loading={loading}
      >
        {title}
      </LoadingButton>
    </Box >
  );
};

export default Viewbutton;
