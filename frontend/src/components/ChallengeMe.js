import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const ChallengeMe = () => {
  const { docId } = useDoc();
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState(["", "", ""]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchQuestions = async () => {
    if (!docId) return;

    setLoading(true);
    setQuestions([]);
    setFeedbacks([]);
    setAnswers(["", "", ""]);

    try {
      const BASE_URL = process.env.REACT_APP_API_BASE_URL;
      const res = await axios.get(`${BASE_URL}/challenge/${docId}`);
      setQuestions(res.data.questions || []);
    } catch (err) {
      console.error("Error fetching questions:", err);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswers = async () => {
    try {
      const BASE_URL = process.env.REACT_APP_API_BASE_URL;
      const res = await axios.post(`${BASE_URL}/challenge/evaluate`, {
        doc_id: docId,
        questions,
        answers,
      });
      setFeedbacks(res.data.feedbacks || []);
    } catch (err) {
      console.error("Error submitting answers:", err);
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
          <button onClick={submitAnswers}>Submit Answers</button>
        </div>
      )}
    </div>
  );
};

export default ChallengeMe;
