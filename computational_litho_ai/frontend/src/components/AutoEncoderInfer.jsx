import React, { useState } from 'react';

function AutoEncoderInfer() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select an image first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/autoencoder/infer", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("AutoEncoder inference failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="my-6 p-4 border border-gray-300 rounded bg-white shadow">
      <h2 className="text-xl font-semibold mb-3">🧩 AutoEncoder Image Inference</h2>

      <input
        type="file"
        accept="image/*"
        className="block mb-3"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        disabled={loading}
      >
        {loading ? "Processing..." : "Run AutoEncoder"}
      </button>

      {result?.message && (
        <div className="mt-4 p-3 bg-gray-100 rounded">
          <p className="text-green-700 font-medium mb-2">✅ {result.message}</p>

          {typeof result.reconstruction_loss === 'number' && (
            <p className="text-sm mb-2">
              <strong>Reconstruction Loss:</strong> {result.reconstruction_loss.toFixed(6)}
            </p>
          )}

          {result.download_zip && (
            <a
              href={`http://127.0.0.1:8000${result.download_zip}`}
              target="_blank"
              rel="noopener noreferrer"
              download
              className="text-blue-600 underline hover:text-blue-800"
            >
              📦 Download ZIP (image + tensor)
            </a>
          )}
        </div>
      )}
    </div>
  );
}

export default AutoEncoderInfer;
