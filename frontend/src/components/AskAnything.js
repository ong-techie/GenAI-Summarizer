import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const AskAnything = () => {
  const { docId } = useDoc();
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const ask = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    if (!docId) {
      setError("No document ID found. Please upload a document first.");
      return;
    }

    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    if (!BASE_URL) {
      setError("API URL not configured. Please set REACT_APP_API_BASE_URL.");
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const res = await axios.post(`${BASE_URL}/ask`, {
        doc_id: docId,
        question,
      });
      setAnswer(res.data.answer || "No answer received.");
    } catch (err) {
      console.error("Error asking question:", err);
      setError(err.response?.data?.detail || "Failed to get answer. Please try again.");
      setAnswer("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" id="ask">
      <h2 className="main-title">💬 Ask Anything</h2>
      <input
        type="text"
        placeholder="Type your question..."
        value={question}
        onChange={(e) => {
          setQuestion(e.target.value);
          setError("");
        }}
        onKeyPress={(e) => {
          if (e.key === "Enter" && !loading) {
            ask();
          }
        }}
      />
      <button onClick={ask} disabled={loading}>
        {loading ? "Asking..." : "Ask"}
      </button>
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
      {answer && (
        <div className="summary-box">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default AskAnything;
