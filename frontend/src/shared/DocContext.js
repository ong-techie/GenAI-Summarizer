import React, { createContext, useContext, useState } from "react";

const DocContext = createContext();

export const DocProvider = ({ children }) => {
  const [docId, setDocId] = useState("");
  return (
    <DocContext.Provider value={{ docId, setDocId }}>
      {children}
    </DocContext.Provider>
  );
};

export const useDoc = () => useContext(DocContext);