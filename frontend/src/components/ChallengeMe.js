import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const ChallengeMe = () => {
  const { docId } = useDoc();
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [feedback, setFeedback] = useState([]);

  const startChallenge = async () => {
    const res = await axios.get(`http://localhost:8000/challenge/${docId}`);
    setQuestions(res.data.questions);
    setAnswers(new Array(res.data.questions.length).fill(""));
    setFeedback([]);
  };

  const submitAnswers = async () => {
    const res = await axios.post("http://localhost:8000/challenge/evaluate", {
      doc_id: docId,
      questions,
      answers
    });
    setFeedback(
      res.data.feedbacks.slice(0, questions.length).map(f => f.trim())
    );
    
  };

  return (
    <div className="card">
      <h2>🧠 Challenge Me</h2>
      <button onClick={startChallenge}>Start Challenge</button>
      {questions.map((q, idx) => (
        <div key={idx} className="qa-box">
          <p><strong>Q{idx + 1}:</strong> {q}</p>
          <input
            type="text"
            placeholder="Your answer"
            value={answers[idx]}
            onChange={(e) => {
              const newAnswers = [...answers];
              newAnswers[idx] = e.target.value;
              setAnswers(newAnswers);
            }}
          />
          {feedback[idx] && <p className="feedback">🗒️ {feedback[idx]}</p>}
        </div>
      ))}
      {questions.length > 0 && <button onClick={submitAnswers}>Submit Answers</button>}
    </div>
  );
};

export default ChallengeMe;