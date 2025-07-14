import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [message, setMessage] = useState("");
  const { setDocId } = useDoc();

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const BASE_URL = process.env.REACT_APP_API_BASE_URL;
      const res = await axios.post(`${BASE_URL}/upload`, formData);
      setDocId(res.data.doc_id);
      setSummary(res.data.summary);
      setMessage("✅ Document uploaded successfully!");
    } catch (error) {
      setMessage("❌ Upload failed. Please try again.");
      console.error("Upload error:", error);
    }
  };

  return (
    <div className="card">
      <h2>📄 Upload Document</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      {message && <p className="feedback">{message}</p>}
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
