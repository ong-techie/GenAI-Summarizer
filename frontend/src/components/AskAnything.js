import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const AskAnything = () => {
  const { docId } = useDoc();
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const res = await axios.post(`${BASE_URL}/ask`, {

      doc_id: docId,
      question
    });
    setAnswer(res.data.answer);
  };

  return (
    <div>
      <h2>Ask Anything</h2>
      <input
        type="text"
        placeholder="Your question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={ask}>Ask</button>
      {answer && <p><strong>Answer:</strong> {answer}</p>}
    </div>
  );
};

export default AskAnything;
