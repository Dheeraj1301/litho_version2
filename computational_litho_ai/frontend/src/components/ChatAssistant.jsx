// frontend/src/components/ChatAssistant.jsx

import React, { useState, useEffect } from 'react';

function ChatAssistant() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [mode, setMode] = useState('doc');
  const [file, setFile] = useState(null);
  const [uploadMsg, setUploadMsg] = useState('');
  const [loading, setLoading] = useState(false);

  // ⬇️ Tensor Analysis
  const [sessionId, setSessionId] = useState('');
  const [availableSessions, setAvailableSessions] = useState([]);
  const [tensorStats, setTensorStats] = useState(null);
  const [tensorError, setTensorError] = useState('');

  // 🔄 Load available sessions once on mount
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/assistant/sessions');
        const data = await res.json();
        if (Array.isArray(data.sessions)) setAvailableSessions(data.sessions);
      } catch (err) {
        console.error('Failed to fetch sessions:', err);
      }
    };

    fetchSessions();
  }, []);

  const handleAsk = async () => {
    if (!input.trim()) return;

    const endpoint = mode === 'tool' ? 'tool' : 'doc';
    setLoading(true);
    setResponse('');

    try {
      const res = await fetch(`http://127.0.0.1:8000/assistant/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });

      if (!res.ok) {
        setResponse(`Assistant endpoint returned ${res.status}. Please restart the backend.`);
        return;
      }

      const data = await res.json();
      setResponse(data.response || 'No assistant response was returned.');
    } catch (err) {
      setResponse('Unable to contact the assistant API. Please confirm the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadMsg('Please choose a PDF first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://127.0.0.1:8000/assistant/upload_pdf', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setUploadMsg(data.message || data.error || 'Upload complete.');
    } catch (err) {
      setUploadMsg('PDF upload failed. Please confirm the backend is running.');
    }
  };

  const handleAnalyzeTensor = async () => {
    setTensorError('');
    setTensorStats(null);
    if (!sessionId) {
      setTensorError('❗ Please select a session.');
      return;
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/assistant/analyze_tensor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!res.ok) {
        const error = await res.json();
        setTensorError(`❌ ${error.detail || 'Tensor analysis failed.'}`);
        return;
      }

      const data = await res.json();
      setTensorStats(data.analysis);
    } catch (err) {
      setTensorError('❌ Error contacting the server.');
    }
  };

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-800">🤖 Data Assistant</h2>
          <p className="mt-1 text-sm text-slate-600">
            Ask about uploaded PDFs, sample CSV/TXT data, lithography concepts, or generated tensor sessions.
          </p>
        </div>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          className="rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm"
        >
          <option value="doc">Ask uploaded/sample data</option>
          <option value="tool">Quick lithography help</option>
        </select>
      </div>

      <div className="mt-4 flex flex-col gap-3 sm:flex-row">
        <input
          type="text"
          className="min-w-0 flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm"
          placeholder="Example: summarize the sample data or explain yield prediction"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') handleAsk();
          }}
        />
        <button
          onClick={handleAsk}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={loading}
        >
          {loading ? 'Asking...' : 'Ask'}
        </button>
      </div>

      {response && (
        <div className="mt-4 rounded-lg border bg-slate-50 p-4 text-sm text-slate-700">
          <strong>Response:</strong> {response}
        </div>
      )}

      <div className="mt-6 grid gap-4 border-t pt-5 lg:grid-cols-2">
        <div>
          <h3 className="text-md font-semibold text-slate-800">📄 Add PDF data</h3>
          <p className="mt-1 text-xs text-slate-500">Uploaded PDFs are saved to the data folder for assistant answers.</p>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="mt-3 w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm file:mr-3 file:rounded-md file:border-0 file:bg-purple-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-purple-700"
          />
          <button
            onClick={handleUpload}
            className="mt-3 rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-purple-700"
          >
            Add to assistant
          </button>
          {uploadMsg && <p className="mt-2 text-sm text-green-700">{uploadMsg}</p>}
        </div>

        <div>
          <h3 className="text-md font-semibold text-slate-800">📊 Analyze tensor session</h3>
          <p className="mt-1 text-xs text-slate-500">Sessions are created by the AutoEncoder reconstruction workflow.</p>
          <select
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            className="mt-3 w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm"
          >
            <option value="">-- Select a session --</option>
            {availableSessions.map((session) => (
              <option key={session} value={session}>{session}</option>
            ))}
          </select>

          <button
            onClick={handleAnalyzeTensor}
            className="mt-3 rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-green-700"
          >
            Analyze Tensor
          </button>

          {tensorError && <p className="mt-2 text-sm text-red-600">{tensorError}</p>}

          {tensorStats && (
            <div className="mt-3 rounded-lg border bg-slate-50 p-3 text-sm">
              <strong>Analysis:</strong>
              <ul className="list-inside list-disc">
                <li><b>Shape:</b> {String(tensorStats.shape)}</li>
                <li><b>Mean:</b> {tensorStats.mean.toFixed(4)}</li>
                <li><b>Std Dev:</b> {tensorStats.std.toFixed(4)}</li>
                <li><b>Min:</b> {tensorStats.min.toFixed(4)}</li>
                <li><b>Max:</b> {tensorStats.max.toFixed(4)}</li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default ChatAssistant;
