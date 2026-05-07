import React, { useState } from 'react';
import axios from 'axios';

function UploadCSV() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a CSV file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://127.0.0.1:8000/upload/', formData);
      alert('✅ File uploaded successfully!');
    } catch (err) {
      alert('❌ Upload failed');
      console.error(err);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <h2 className="text-xl font-semibold text-slate-800">📁 CSV Upload</h2>
      <p className="mt-1 text-sm text-slate-600">
        Upload production/process CSV files to prepare data for downstream predictions.
      </p>

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-700 file:mr-3 file:rounded-md file:border-0 file:bg-blue-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-blue-700"
        />
        <button
          onClick={handleUpload}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
        >
          Upload CSV
        </button>
      </div>

      {file && <p className="mt-3 text-xs text-slate-500">Selected file: {file.name}</p>}
    </section>
  );
}

export default UploadCSV;
