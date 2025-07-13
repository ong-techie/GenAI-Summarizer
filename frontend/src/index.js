import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { DocProvider } from "./shared/DocContext";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <DocProvider>
      <App />
    </DocProvider>
  </BrowserRouter>
);