import React from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/Homepage";
import "./index.css";

const App = () => {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </div>
  );
};

export default App;