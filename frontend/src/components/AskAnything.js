import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const AskAnything = () => {
  const { docId } = useDoc();
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    if (!question.trim()) return;
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const res = await axios.post(`${BASE_URL}/ask`, {
      doc_id: docId,
      question,
    });
    setAnswer(res.data.answer);
  };

  return (
    <div className="card" id="ask">
      <h2 className="main-title">💬 Ask Anything</h2>
      <input
        type="text"
        placeholder="Type your question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={ask}>Ask</button>
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
