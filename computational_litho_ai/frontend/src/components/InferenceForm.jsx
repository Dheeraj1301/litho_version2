import React, { useState } from 'react';

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
      setError('Please select a CSV file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/inference/run', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      if (res.ok && !data.error) {
        setResult(data);
      } else {
        setError(`❌ Inference error: ${data.error || data.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`❌ Network error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!Array.isArray(result?.rows_received) || result.rows_received.length === 0) return;

    const csv = [
      Object.keys(result.rows_received[0]).join(','),
      ...result.rows_received.map((row) => Object.values(row).join(',')),
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'inference_result.csv';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <h2 className="text-xl font-semibold text-slate-800">🔬 CSV Yield Inference</h2>
      <p className="mt-1 text-sm text-slate-600">
        Upload a CSV file once, run the yield model, then download the prediction output.
      </p>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="mt-4 w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-700 file:mr-3 file:rounded-md file:border-0 file:bg-blue-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-blue-700"
      />

      {selectedFile && <p className="mt-2 text-xs text-slate-500">Selected file: {selectedFile.name}</p>}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          onClick={handleInference}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={loading}
          title={!selectedFile ? 'Upload a CSV file first' : 'Run inference'}
        >
          {loading ? 'Processing...' : 'Run Inference'}
        </button>

        {Array.isArray(result?.rows_received) && result.rows_received.length > 0 && (
          <button
            onClick={downloadCSV}
            className="rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-green-700"
          >
            Download CSV
          </button>
        )}
      </div>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
          {error}
        </div>
      )}

      {Array.isArray(result?.rows_received) && result.rows_received.length > 0 && (
        <div className="mt-6 overflow-x-auto">
          <h3 className="mb-2 text-lg font-semibold text-slate-800">📊 Inference Output</h3>
          <table className="min-w-full table-auto border border-slate-300 text-sm">
            <thead className="bg-slate-100">
              <tr>
                {Object.keys(result.rows_received[0]).map((key) => (
                  <th key={key} className="border px-4 py-2 text-left font-semibold text-slate-700">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.rows_received.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  {Object.values(row).map((val, jdx) => (
                    <td key={jdx} className="border px-4 py-2 text-slate-700">{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {Array.isArray(result?.rows_received) && result.rows_received.length === 0 && (
        <div className="mt-4 rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-sm text-yellow-800">
          ⚠️ No results were returned from inference.
        </div>
      )}
    </section>
  );
}

export default InferenceForm;
