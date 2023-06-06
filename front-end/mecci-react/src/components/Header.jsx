import { Typography, useTheme } from "@mui/material";
import { tokens } from "../theme";

const Header = ({ title }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Typography
      variant="h1"
      color={colors.greenAccent[200]}
      fontWeight="bold"
      align="center"
      sx={{ mb: "15px" }}
    >
      {title}
    </Typography>
  );
};

export default Header;
