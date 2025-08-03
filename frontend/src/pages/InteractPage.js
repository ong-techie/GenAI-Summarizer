import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AskAnything from "../components/AskAnything";
import ChallengeMe from "../components/ChallengeMe";
import Navbar from "../components/navbar";
import { useDoc } from "../shared/DocContext";

const InteractPage = () => {
  const { docId, summary } = useDoc();
  const navigate = useNavigate();

  // Redirect to homepage if docId is missing
  useEffect(() => {
    if (!docId) {
      navigate("/");
    }
  }, [docId, navigate]);

  return (
    <>
      <Navbar />
      <div className="container">
        <h1 className="main-title">🧠 Interact with Your Document</h1>

        {summary && (
          <div className="summary-box" style={{ marginBottom: "30px" }}>
            <strong>📝 Summary:</strong>
            <p>{summary}</p>
          </div>
        )}

        <AskAnything />
        <ChallengeMe />
      </div>
    </>
  );
};

export default InteractPage;
