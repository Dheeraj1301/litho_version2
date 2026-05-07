import React, { useState } from 'react';

function ImageInference() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResult(null);
  };

  const handleClassify = async () => {
    if (!selectedFile) {
      setResult({ error: 'Please select an image first.' });
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await fetch('http://127.0.0.1:8000/inference/image/classify', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: 'Image classification failed. Please confirm the backend is running.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <h2 className="text-xl font-semibold text-slate-800">🖼️ Image Classification</h2>
      <p className="mt-1 text-sm text-slate-600">
        Classify a layout image. Use the AutoEncoder panel below for reconstruction and tensor downloads.
      </p>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mt-4 w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm text-slate-700 file:mr-3 file:rounded-md file:border-0 file:bg-blue-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-blue-700"
      />

      <button
        onClick={handleClassify}
        className="mt-3 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={loading}
      >
        {loading ? 'Classifying...' : 'Classify Image'}
      </button>

      {result && (
        <div className="mt-4 rounded-lg border bg-slate-50 p-4 text-sm">
          {result.error ? (
            <p className="text-red-600">{result.error}</p>
          ) : (
            <>
              <p className="font-medium text-green-700">✅ {result.message}</p>
              {result.predicted_class !== undefined && (
                <p className="mt-2 text-slate-700">
                  <strong>Predicted class:</strong> {result.predicted_class}
                </p>
              )}
            </>
          )}
        </div>
      )}
    </section>
  );
}

export default ImageInference;
