// frontend/src/components/ChatAssistant.jsx

import React, { useState, useEffect } from 'react';

function ChatAssistant() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [mode, setMode] = useState("tool");
  const [file, setFile] = useState(null);
  const [uploadMsg, setUploadMsg] = useState("");

  // ⬇️ Tensor Analysis
  const [sessionId, setSessionId] = useState("");
  const [availableSessions, setAvailableSessions] = useState([]);
  const [tensorStats, setTensorStats] = useState(null);
  const [tensorError, setTensorError] = useState("");

  // 🔄 Load available sessions once on mount
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/assistant/sessions");
        const data = await res.json();
        if (data.sessions) setAvailableSessions(data.sessions);
      } catch (err) {
        console.error("Failed to fetch sessions:", err);
      }
    };

    fetchSessions();
  }, []);

  const handleAsk = async () => {
    if (!input) return;

    const endpoint = mode === "tool" ? "tool" : "doc";

    const res = await fetch(`http://127.0.0.1:8000/assistant/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input }),
    });

    const data = await res.json();
    setResponse(data.response);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/assistant/upload_pdf", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setUploadMsg(data.message);
  };

  const handleAnalyzeTensor = async () => {
    setTensorError("");
    setTensorStats(null);
    if (!sessionId) {
      setTensorError("❗ Please select a session.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/assistant/analyze_tensor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!res.ok) {
        const error = await res.json();
        setTensorError(`❌ ${error.detail}`);
        return;
      }

      const data = await res.json();
      setTensorStats(data.analysis);
    } catch (err) {
      setTensorError("❌ Error contacting the server.");
    }
  };

  return (
    <div className="p-4 border rounded bg-white shadow mt-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">🤖 AI Assistant</h2>

      {/* Mode Selector */}
      <div className="mb-4">
        <label className="text-sm font-medium mr-2">Mode:</label>
        <select value={mode} onChange={(e) => setMode(e.target.value)} className="border px-2 py-1 rounded">
          <option value="tool">LangChain Tool</option>
          <option value="doc">Doc QA</option>
        </select>
      </div>

      {/* Question Input */}
      <input
        type="text"
        className="border p-2 rounded w-full mb-3"
        placeholder="Ask me anything..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      {/* Ask Button */}
      <button
        onClick={handleAsk}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mb-4"
      >
        Ask
      </button>

      {/* Assistant Response */}
      {response && (
        <div className="bg-gray-100 p-3 rounded text-sm border">
          <strong>Response:</strong> {response}
        </div>
      )}

      {/* PDF Upload Section */}
      <div className="mt-6 border-t pt-4">
        <h3 className="text-md font-semibold mb-2">📄 Upload PDF to Knowledge Base</h3>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} className="mb-2" />
        <button
          onClick={handleUpload}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Upload
        </button>
        {uploadMsg && <p className="text-sm mt-2 text-green-700">{uploadMsg}</p>}
      </div>

      {/* Tensor Session Analysis */}
      <div className="mt-6 border-t pt-4">
        <h3 className="text-md font-semibold mb-2">📊 Analyze Tensor from Session</h3>

        <select
          value={sessionId}
          onChange={(e) => setSessionId(e.target.value)}
          className="border p-2 rounded w-full mb-2"
        >
          <option value="">-- Select a session --</option>
          {availableSessions.map((session) => (
            <option key={session} value={session}>{session}</option>
          ))}
        </select>

        <button
          onClick={handleAnalyzeTensor}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Analyze Tensor
        </button>

        {tensorError && <p className="text-sm text-red-600 mt-2">{tensorError}</p>}

        {tensorStats && (
          <div className="bg-gray-50 p-3 mt-3 rounded text-sm border">
            <strong>Analysis:</strong>
            <ul className="list-disc list-inside">
              <li><b>Shape:</b> {tensorStats.shape}</li>
              <li><b>Mean:</b> {tensorStats.mean.toFixed(4)}</li>
              <li><b>Std Dev:</b> {tensorStats.std.toFixed(4)}</li>
              <li><b>Min:</b> {tensorStats.min.toFixed(4)}</li>
              <li><b>Max:</b> {tensorStats.max.toFixed(4)}</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatAssistant;
