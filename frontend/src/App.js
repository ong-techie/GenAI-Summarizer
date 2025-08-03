import React from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/Homepage";
import InteractPage from "./pages/InteractPage"; // new import
import "./index.css";

const App = () => {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/interact" element={<InteractPage />} /> {/* new route */}
      </Routes>
    </div>
  );
};

export default App;
