import React from "react";
import UploadForm from "../components/UploadForm";
import AskAnything from "../components/AskAnything";
import ChallengeMe from "../components/ChallengeMe";

const HomePage = () => {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Document QA Assistant</h1>
      <UploadForm />
      <AskAnything />
      <ChallengeMe />
    </div>
  );
};
export default HomePage;