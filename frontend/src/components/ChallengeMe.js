import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const ChallengeMe = () => {
  const { docId } = useDoc();
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState(["", "", ""]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const fetchQuestions = async () => {
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
    setQuestions([]);
    setFeedbacks([]);
    setAnswers(["", "", ""]);

    try {
      const res = await axios.get(`${BASE_URL}/challenge/${docId}`);
      setQuestions(res.data.questions || []);
      if (!res.data.questions || res.data.questions.length === 0) {
        setError("No questions could be generated for this document.");
      }
    } catch (err) {
      console.error("Error fetching questions:", err);
      setError(err.response?.data?.detail || "Failed to generate questions. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const submitAnswers = async () => {
    if (!docId) {
      setError("No document ID found. Please upload a document first.");
      return;
    }

    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    if (!BASE_URL) {
      setError("API URL not configured. Please set REACT_APP_API_BASE_URL.");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      const res = await axios.post(`${BASE_URL}/challenge/evaluate`, {
        doc_id: docId,
        questions,
        answers,
      });
      setFeedbacks(res.data.feedbacks || []);
    } catch (err) {
      console.error("Error submitting answers:", err);
      setError(err.response?.data?.detail || "Failed to submit answers. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="card">
      <h2 className="main-title">🧠 Challenge Yourself</h2>
      <button onClick={fetchQuestions} disabled={loading}>
        {loading ? "Loading..." : "Generate Challenge Questions"}
      </button>
      {questions.length > 0 && (
        <div className="challenge-block">
          {questions.map((q, idx) => (
            <div key={idx} className="question-block">
            <p><strong>Q{idx + 1}:</strong> {q.replace(/^(\d+\.\s*)/, '')}</p>
            <textarea
              className="answer-box"
              placeholder="Type your answer here..."
              value={answers[idx]}
              onChange={(e) => {
                const newAnswers = [...answers];
                newAnswers[idx] = e.target.value;
                setAnswers(newAnswers);
              }}
            />
            {feedbacks[idx] && (
              <p className="feedback">Feedback: {feedbacks[idx]}</p>
            )}
          </div>
          ))}
          <button onClick={submitAnswers} disabled={submitting}>
            {submitting ? "Submitting..." : "Submit Answers"}
          </button>
        </div>
      )}
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
    </div>
  );
};

export default ChallengeMe;
