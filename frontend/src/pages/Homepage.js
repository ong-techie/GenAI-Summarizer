import React from "react";
import UploadForm from "../components/UploadForm";
import Navbar from "../components/Navbar";

const HomePage = () => {
  return (
    <>
      <Navbar />
      <div className="container">
        <h1 className="main-title">📚 Document QA Assistant</h1>
        <UploadForm />
      </div>
    </>
  );
};

export default HomePage;
