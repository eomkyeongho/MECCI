import { useMemo, useState, createContext } from "react";

const FileContext = createContext({
  filename: "",
  setFilename: () => {},
  iac: "",
  setIac: () => {},
  mutated: "",
  setMutated: () => {},
});

const FileProvider = ({ children }) => {
  const [filename, setFilename] = useState("");
  const [iac, setIac] = useState("");
  const [mutated, setMutated] = useState("");

  const value = useMemo(
    () => ({ filename, setFilename, iac, setIac, mutated, setMutated }),
    [filename, setFilename, iac, setIac, mutated, setMutated]
  );

  return <FileContext.Provider value={value}>{children}</FileContext.Provider>;
};

export { FileContext, FileProvider };
