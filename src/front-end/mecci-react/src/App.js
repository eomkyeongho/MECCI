import React from "react";
import { Routes, Route } from "react-router-dom";
import { CssBaseline, ThemeProvider } from "@mui/material";

import { ColorModeContext, useMode } from "./theme";
import Topbar from "./scenes/global/Topbar";
import Viewcode from "./scenes/viewcode";
import Select from "./scenes/select";
import FileUpload from "./scenes/fileupload";
import { FileProvider } from "./context/context";

function App() {
  const [theme, colorMode] = useMode();

  return (
    <ColorModeContext.Provider value={colorMode}>
      <FileProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <div className="app">
            <main className="contents" style={{ zIndex: "2" }}>
              <Topbar />
              <Routes>
                <Route path="/" element={<Select />} />
                <Route path="/viewcode" element={<Viewcode />} />
              </Routes>
            </main>
          </div>
        </ThemeProvider>
      </FileProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
