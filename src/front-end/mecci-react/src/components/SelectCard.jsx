import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { Typography, useTheme, Box } from "@mui/material";
import AdsClickIcon from "@mui/icons-material/AdsClick";
import { tokens } from "../theme";
import Tilt from "react-parallax-tilt";
import "./SelectCard.css";

const SelectCard = ({ title, src, num, click }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [isHover, setIsHover] = useState(false);
  const test = `<h2>02</h2>
  <h3>Card Two</h3>
  <p>testasdfgsdaf asdf</p>
  <a href="#">read</a>`;
  return (
    <div className="container">
      <Tilt glareEnable="true" glareMaxOpacity="1" transitionSpeed="400">
        {/* <Link to={to}> */}
        <div
          className="card"
          onMouseOver={() => {
            setIsHover(true);
          }}
          onMouseOut={() => {
            setIsHover(false);
          }}
          onClick={click}
        >
          {!isHover && (
            <Box>
              <img className="picture" src={src} />
              <Typography
                variant="h3"
                color={colors.blueAccent[200]}
                sx={{ textAlign: "center", fontWeight: "bold" }}
              >
                {title}
              </Typography>
            </Box>
          )}
          <div className="content">
            {isHover && (
              <div>
                <h2>{num}</h2>
              </div>
            )}
          </div>
        </div>
        {/* </Link> */}
      </Tilt>
    </div>
  );
};

export default SelectCard;
