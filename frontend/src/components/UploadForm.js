import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const { setDocId } = useDoc();

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("https://genai-summarizer-1-bpn5.onrender.com/upload", formData);
    setDocId(res.data.doc_id);
    setSummary(res.data.summary);
    alert("Upload successful. Doc ID: " + res.data.doc_id);
  };

  return (
    <div className="card">
      <h2>📄 Upload Document</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      {summary && (
        <div className="summary-box">
          <strong>📝 Summary:</strong>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
