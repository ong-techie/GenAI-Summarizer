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
    const res = await axios.post("http://localhost:8000/upload", formData);
    setDocId(res.data.doc_id);
    setSummary(res.data.summary);
    alert("Upload successful. Doc ID: " + res.data.doc_id);
  };

  return (
    <div>
      <h2>Upload Document</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      {summary && (
        <div style={{ marginTop: "10px" }}>
          <strong>Summary:</strong>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
};

export default UploadForm;