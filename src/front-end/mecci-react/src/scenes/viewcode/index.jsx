import React, { useState, useContext, useRef, useEffect } from "react";

import { tokens } from "../../theme";
import Header from "../../components/Header";
import client from "../../utils/clients";
import Viewbutton from "../../components/Viewbutton";
import { FileContext } from "../../context/context";
import ModalDialog from "../../components/ModalDialog";
import Validate from "../../components/Validate";

import Prismjs from "prismjs"
import "prismjs/components/prism-hcl";
import "prismjs/themes/prism-dark.css";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { materialDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Box, useTheme, Card, Typography } from "@mui/material";
import ReactDiffViewer, { DiffMethod } from "react-diff-viewer-continued";
import { GiCycle } from "react-icons/gi";
import VerifiedIcon from '@mui/icons-material/Verified';
import HubIcon from '@mui/icons-material/Hub';
import DoneIcon from '@mui/icons-material/Done';
import ClearIcon from '@mui/icons-material/Clear';
// import { socket, initSocketConnection } from "../../utils/socket"

import { io } from "socket.io-client";

const Viewcode = () => {

  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const scrollRef = useRef();

  const { filename, setFilename, iac, setIac, mutated, setMutated } =
    useContext(FileContext);
  const [open, setOpen] = useState(false);
  const [result, setResult] = useState(false);

  const [mutBut, setMutBut] = useState(false);

  const [diffBut, setDiffBut] = useState("disabled");
  const [graphBut, setGraphBut] = useState("disabled");
  const [scriptBut, setScriptBut] = useState("disabled");
  const [genBut, setGenBut] = useState("disabled");
  const [valBut, setValBut] = useState("disabled");

  const [mutlodingBut, setMutlodingBut] = useState(false);
  const [graphlodingBut, setGraphlodingBut] = useState(false);
  const [injectlodingBut, setInjectlodingBut] = useState(false);
  const [validatelodingBut, setValidatelodingBut] = useState(false);
  const [genlodingBut, setGenlodingBut] = useState(false);

  // const [diffBut, setDiffBut] = useState(undefined);
  // const [graphBut, setGraphBut] = useState(undefined);
  // const [scriptBut, setScriptBut] = useState(undefined);
  // const [genBut, setGenBut] = useState(undefined);
  // const [valBut, setValBut] = useState(undefined);

  const [validate, setValidate] = useState(false);

  const [svgmodal, setSvgmodal] = useState(false);
  const [originsvg, setOriginsvg] = useState("");
  const [mutatedsvg, setMutatedsvg] = useState("");

  const [test, setTest] = useState(false);

  const [validateColor, setValidateColor] = useState("red");

  const [soc, setSoc] = useState(false);
  const [dis, setDis] = useState(true);

  const [before, setBefor] = useState("");
  const [after, setAfter] = useState("");
  const [inject, setInject] = useState(false);

  let socket = "";

  const serverURL = "http://211.117.84.151:8082/static/"

  const url = "http://121.135.134.175/dashboard/project/network_topology/"

  const scrollToBottom = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
    scrollRef.current.style.overflow = "scroll";
  }, [mutated]);

  // useEffect(() => {
  //   scrollRef.current.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
  // }, [mutated])

  useEffect(
    () => {
      socket = io("http://211.117.84.151:8083", { transports: ['websocket', 'polling', 'flashsocket'] });
      setMutated("")
      socket.connect();
      socket.on("my_response", (data) => {
        if (data.data === "Connected" || data.data === null)
          console.log(data);
        else {
          setMutated((prev) => prev + data.data);
        }
      });
      return (
        () => {
          socket.disconnect()
        }
      )
    },
    [soc]
  )

  // useEffect(
  //   () => {
  //     socket.off("my_response");
  //   }, []
  // )
  const handleMutatedButton = async () => {
    setSoc((prev) => !prev);
    setMutlodingBut(true);
    setMutated("")
    setDiffBut("disabled");
    setGraphBut("disabled");
    setValBut("disabled");
    setScriptBut("disabled");
    setGenBut("disabled");
    try {
      console.log("diffstart");
      const res = await client.get(`/mutation?fileName=${filename}`);
      setOriginsvg("");
      setMutated(res.data.mutated);
      setIac(res.data.origin);
      setMutated(res.data.mutated);
      setDiffBut(undefined);
      setValBut(undefined);
      setDis(false);
    } catch (err) {
      console.log(err);
      setMutated(err + "\n" + "Retry Mutated");
    }
    setMutlodingBut(false);
  };

  const handleDiffButton = () => {
    setOpen((prev) => !prev);
  };

  const handleGraphButton = async () => {
    if (originsvg == "") {
      setGraphlodingBut(true);
      try {
        const res = await client.get("/visualize-iac");
        setOriginsvg(res.data.origin_svg.replace(/\\/g, ""));
        setMutatedsvg(res.data.mutated_svg.replace(/\\/g, ""));
        setSvgmodal(true);
      } catch (err) {
        console.log(err);
      }
    }
    else {
      setSvgmodal((prev) => !prev);
    }
    setGraphlodingBut(false);
  };

  const handleInjectButton = async () => {
    setInjectlodingBut(true);
    setInject((prev) => !prev);

    setAfter(mutated);
    try {
      const res = await client.get("/injection");
      console.log(res.data.injected);
      setMutated(res.data.injected);
      setBefor(res.data.injected);
    } catch (err) {
      console.log(err);
    }
    setInjectlodingBut(false);
  }

  const handleValidateButton = async () => {
    setValidatelodingBut(true);
    try {
      const res = await client.get("/validation");
      if (res.data.result === "fail")
        setValidateColor("red");
      else {
        setValidateColor("green");
        setGraphBut(undefined);
        setScriptBut(undefined);
        setGenBut(undefined)
      }
    } catch (err) {
      console.log(err);
    }
    console.log(test);
    setTest(true);
    setValidatelodingBut(false)
  }

  const handleGenerateButton = async () => {
    window.open(url);
    setGenlodingBut(true);
    try {
      const res = await client.get("/terraform-apply");
      console.log(res);
    }
    catch (err) {
      console.log(err);
    }
    setGenlodingBut(false);
  }


  const highlightSyntax = (str) => {
    return (
      <SyntaxHighlighter
        language="hcl"
        style={materialDark}
        customStyle={{
          margin: 0,
          padding: 0,
          background: "transparent",
        }}
      >
        {str}
      </SyntaxHighlighter>);
  };

  const diffView = (
    <Box display="flex"
      gridColumn="span 12"
      gridRow="span 14"
      alignItems="center"
      borderRadius="40px"
      sx={{
        margin: "10px",
        background: `${colors.primary[400]}`,
      }}>
      <Card
        sx={{
          display: "flex",
          width: "100%",
          height: "90%",
          margin: "3%",
          borderRadius: "20px",
          boxShadow: "4px 4px 16px 16px rgba(0, 0, 0, 0.2)",
          background: "#2f2f2f",
          overflow: "scroll",
        }}
      >
        <ReactDiffViewer
          oldValue={iac}
          newValue={mutated}
          splitView={true}
          compareMethod={DiffMethod.WORDS}
          renderContent={highlightSyntax}
          useDarkTheme={true}
          styles={{
            // contentText: {
            //   backgroundColor: "transparent",
            // },
          }}
        />
      </Card>
    </Box>
  );

  return (
    <>
      <Box
        marginLeft="50px"
        marginTop="10px"
        sx={{
          "& ::-webkit-scrollbar": {
            visibility: "hidden",
          },
          "& ::-webkit-scrollbar:hover": {
            display: "invisible",
          },
        }}
      >
        <Box
          display="grid"
          gridTemplateColumns="repeat(15, 1fr)"
          gridAutoRows="35px"
          gap="15px"
        >
          <Box
            gridColumn="span 6"
            alignItems="center"
            justifyContent="center"
            verticalalign="middle"
          >
            <Header title="Origin" />
          </Box>
          <Box
            gridColumn="span 6"
            alignItems="center"
            justifyContent="center"
            verticalalign="middle"
          >
            <Header title="Mutated" />
          </Box>
          {test && (
            <ModalDialog
              open={test}
              handleClose={() => setTest((prev) => !prev)}
              title="Validate"
              styled={"1000px"}
            >
              <Box display="flex" sx={{ color: validateColor }}>
                <Box sx={{ float: "left", width: "33%", textAlign: "center" }}
                >
                  <GiCycle size="5rem" />
                  <Typography sx={{ fontWeight: "bold", color: "#FFF" }}>Consistency Test</Typography>
                  {`${validateColor}` === "red" ? <ClearIcon /> : <DoneIcon />}
                </Box>
                <Box sx={[{ float: "left", width: "33%", textAlign: "center" },
                  "svg":{
                }]}>
                <VerifiedIcon sx={{ fontSize: "5rem" }} />
                <Typography sx={{ fontWeight: "bold", color: "#FFF" }}>Validity Test</Typography>
                {`${validateColor}` === "red" ? <ClearIcon /> : <DoneIcon />}
              </Box>
              <Box sx={{ float: "left", width: "33%", textAlign: "center" }}>
                <HubIcon sx={{ fontSize: "5rem" }} />
                <Typography sx={{ fontWeight: "bold", color: "#FFF" }}>Features Extracting</Typography>
                {`${validateColor}` === "red" ? <ClearIcon /> : <DoneIcon />}
              </Box>
            </Box>
            </ModalDialog>
            )}
        {open && diffView}
        {!open && !svgmodal && (
          <>
            <Box
              display="flex"
              gridColumn="span 6"
              gridRow="span 14"
              alignItems="center"
              borderRadius="40px"
              sx={{
                margin: "10px",
                background: `${colors.primary[400]}`,
              }}
            >
              <Card
                sx={{
                  display: "flex",
                  width: "100%",
                  height: "90%",
                  margin: "6%",
                  borderRadius: "20px",
                  boxShadow: "4px 4px 16px 16px rgba(0, 0, 0, 0.2)",
                  background: "#2f2f2f",
                }}
              >
                <SyntaxHighlighter
                  showLineNumbers
                  language="hcl"
                  style={materialDark}
                >
                  {iac}
                </SyntaxHighlighter>
              </Card>
            </Box>
            <Box
              display="flex"
              gridColumn="span 6"
              gridRow="span 14"
              alignItems="center"
              borderRadius="40px"
              sx={{
                margin: "10px",
                background: `${colors.primary[400]}`,
              }}
            >
              <Card
                ref={scrollRef}
                sx={{
                  display: "flex",
                  height: "90%",
                  width: "100%",
                  margin: "6%",
                  borderRadius: "20px",
                  boxShadow: "4px 4px 16px 16px rgba(0, 0, 0, 0.2)",
                  background: "#2f2f2f",
                }}>
                <Box ref={scrollRef}>
                  <SyntaxHighlighter
                    language="hcl"
                    showLineNumbers
                    style={materialDark}
                  >
                    {mutated}
                  </SyntaxHighlighter>
                </Box>
              </Card>
            </Box>
          </>
        )}
        {svgmodal && (
          <>
            <Box
              display="flex"
              gridColumn="span 6"
              gridRow="span 14"
              alignItems="center"
              borderRadius="40px"
              sx={{
                margin: "10px",
                background: `${colors.primary[400]}`,
              }}
            >
              <Card
                sx={{
                  display: "flex",
                  width: "100%",
                  textAlign: "center",
                  alignItems: "center",
                  justifyContent: "center",
                  height: "90%",
                  margin: "6%",
                  borderRadius: "20px",
                  boxShadow: "4px 4px 16px 16px rgba(0, 0, 0, 0.2)",
                  background: "#2f2f2f",
                }}
              >
                <img style={{ width: "90%" }} alt="origins-vg" src={`${serverURL}/origin.svg`} />
              </Card>
            </Box>
            <Box
              display="flex"
              gridColumn="span 6"
              gridRow="span 14"
              alignItems="center"
              borderRadius="40px"
              sx={{
                margin: "10px",
                background: `${colors.primary[400]}`,
              }}
            >
              <Card
                sx={{
                  display: "flex",
                  height: "90%",
                  width: "100%",
                  margin: "6%",
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: "20px",
                  boxShadow: "4px 4px 16px 16px rgba(0, 0, 0, 0.2)",
                  background: "#2f2f2f",
                }}
              >
                <img style={{ width: "90%" }} alt="mutated-vg" src={`${serverURL}/mutated.svg`} />
              </Card>
            </Box>
          </>
        )}
        {inject && (
          <ModalDialog
            open={inject}
            handleClose={() => setInject((prev) => !prev)}
            title="Before & After"
            // title="Validate"
            styled={"1000px"}>
            <ReactDiffViewer
              oldValue={before}
              newValue={after}
              splitView={false}
              compareMethod={DiffMethod.WORDS}
              renderContent={highlightSyntax}
              useDarkTheme={true}
              styles={{
                // contentText: {
                //   backgroundColor: "transparent",
                // },
              }}
            />
          </ModalDialog>
        )}
        <Box sx={{ gridColumn: "span 3" }} />
        <Viewbutton
          title="Validate"
          height="70%"
          width="70%"
          color="grey[100]"
          col="span 3"
          row="span 3"
          disabled={valBut}
          loading={validatelodingBut}
          click={handleValidateButton}
        />
        <Viewbutton
          title="show diff"
          height="70%"
          width="70%"
          color="grey[100]"
          col="span 3"
          row="span 3"
          disabled={diffBut}
          click={handleDiffButton}
        />
        <Viewbutton
          title="Show Graph"
          height="70%"
          color="grey[100]"
          width="70%"
          col="span 3"
          row="span 3"
          click={handleGraphButton}
          disabled={graphBut}
          loading={graphlodingBut}
        />
        <Viewbutton
          title="Inject Script"
          height="70%"
          width="70%"
          color="grey[100]"
          col="span 3"
          row="span 3"
          disabled={scriptBut}
          loading={injectlodingBut}
          click={handleInjectButton}
        />
      </Box >
      <Box
        display="grid"
        gridTemplateColumns="repeat(2, 1fr)"
        gridTemplateRows="repeat(1, 1fr)"
        sx={{
          mt: "15px",
          height: "10vh",
          mr: "20%"
        }}
      >
        <Viewbutton
          title="Mutate"
          color="grey[100]"
          width="100%"
          height="108px"
          click={handleMutatedButton}
          loading={mutlodingBut}

        />
        <Viewbutton
          title="Generate"
          width="100%"
          height="108px"
          color="grey[100]"
          disabled={genBut}
          click={handleGenerateButton}
          loading={genlodingBut}
        />
      </Box>
    </Box >
      {/* {test && <Validate open={test} close={() => setTest((prev) => !prev)}>test</Validate>} */ }
    </>
  );
};

export default Viewcode;
