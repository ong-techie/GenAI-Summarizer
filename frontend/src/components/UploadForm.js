import React, { useState } from "react";
import axios from "axios";
import { useDoc } from "../shared/DocContext";
import { useNavigate } from "react-router-dom";


const UploadForm = () => {
  const navigate = useNavigate(); // at top of UploadForm component

  const [file, setFile] = useState(null);
  const { setDocId, setSummary } = useDoc();
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      setMessage("");
      setSummary("");

      const BASE_URL = process.env.REACT_APP_API_BASE_URL;
      const res = await axios.post(`${BASE_URL}/upload`, formData);

      if (res.data.doc_id && res.data.summary) {
        setDocId(res.data.doc_id);
        setSummary(res.data.summary);
        console.log("✅ Uploaded doc_id:", res.data.doc_id); // <-- This line
        navigate("/interact");
              

      } else {
        setMessage("❌ Upload failed. Invalid server response.");
      }
    } catch (error) {
      setMessage("❌ Upload failed. Please try again.");
      console.error("Upload error:", error);
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setSummary("");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setMessage("");
      setSummary("");
    }
  };

  return (
    <div className="card" id="upload">
      <h2 className="main-title">📄 Upload Document</h2>

      <div
        className={`dropzone ${isDragging ? "drag-over" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <p>{file ? `Selected: ${file.name}` : "Drag & drop a file here or click to choose"}</p>
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={handleFileChange}
          style={{ display: "none" }}
          id="fileUploadInput"
        />
        <label htmlFor="fileUploadInput" className="upload-label">Choose File</label>
      </div>

      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? <div className="spinner"></div> : "Upload"}
      </button>

      {message && <p className="feedback">{message}</p>}
      
    </div>
  );
};

export default UploadForm;
