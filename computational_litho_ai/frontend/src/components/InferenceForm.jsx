import React, { useState } from "react";
import { Tooltip } from "react-tooltip"; // ✅ Correct import for react-tooltip
import "react-tooltip/dist/react-tooltip.css"; // ✅ Required CSS

function InferenceForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleInference = async () => {
    if (!selectedFile) {
      setError("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/inference/run", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (res.ok) {
        setResult(data);
      } else {
        setError("❌ Inference error: " + (data.error || "Unknown error"));
      }
    } catch (err) {
      setError("❌ Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!Array.isArray(result?.rows_received) || result.rows_received.length === 0) return;

    const csv = [
      Object.keys(result.rows_received[0]).join(","), // header
      ...result.rows_received.map((row) => Object.values(row).join(",")), // rows
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "inference_result.csv";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white p-6 rounded shadow-md mt-4">
      <h2 className="text-xl font-semibold mb-4">🔬 Run Inference</h2>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="mb-4 border p-2 rounded w-full"
      />

      <div className="flex gap-4">
        <button
          onClick={handleInference}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          disabled={loading}
          data-tooltip-id="tip"
          data-tooltip-content={!selectedFile ? "Upload a file first" : ""}
        >
          {loading ? "Processing..." : "Run Inference"}
        </button>

        {Array.isArray(result?.rows_received) && result.rows_received.length > 0 && (
          <button
            onClick={downloadCSV}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
          >
            Download CSV
          </button>
        )}
      </div>

      <Tooltip id="tip" />

      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-800 rounded">
          ⚠️ {error}
        </div>
      )}

      {Array.isArray(result?.rows_received) && result.rows_received.length > 0 && (
        <div className="mt-6 overflow-x-auto">
          <h3 className="text-lg font-semibold mb-2">📊 Inference Output</h3>
          <table className="min-w-full table-auto border border-gray-300">
            <thead className="bg-gray-200">
              <tr>
                {Object.keys(result.rows_received[0]).map((key) => (
                  <th key={key} className="px-4 py-2 border">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.rows_received.map((row, idx) => (
                <tr key={idx} className="hover:bg-gray-100">
                  {Object.values(row).map((val, jdx) => (
                    <td key={jdx} className="px-4 py-2 border">{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {Array.isArray(result?.rows_received) && result.rows_received.length === 0 && (
        <div className="mt-4 p-4 bg-yellow-100 border border-yellow-400 text-yellow-800 rounded">
          ⚠️ No results were returned from inference.
        </div>
      )}
    </div>
  );
}

export default InferenceForm;
