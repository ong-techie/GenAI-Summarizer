import React, { createContext, useContext, useState } from "react";

const DocContext = createContext();

export const DocProvider = ({ children }) => {
  const [docId, setDocId] = useState("");
  const [summary, setSummary] = useState(""); // ✅ Add this line

  return (
    <DocContext.Provider value={{ docId, setDocId, summary, setSummary }}>
      {children}
    </DocContext.Provider>
  );
};

export const useDoc = () => useContext(DocContext);
