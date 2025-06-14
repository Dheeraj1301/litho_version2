import React, { useState } from 'react';

function ImageInference() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResult(null);
  };

  const handleSubmit = async (endpoint) => {
    if (!selectedFile) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await fetch(`http://127.0.0.1:8000/inference/${endpoint}`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();

      // If tensor_array is present, don't display it
      if ('tensor_array' in data) {
        delete data.tensor_array;
      }

      setResult(data);
    } catch (error) {
      setResult({ error: 'Upload failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-6 border-t pt-6">
      <h2 className="text-xl font-semibold text-gray-700 mb-2">🖼️ Image Inference</h2>

      <input type="file" accept="image/*" onChange={handleFileChange} className="mb-2" />

      <div className="space-x-2">
        <button
          onClick={() => handleSubmit('image/classify')}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Classify Image
        </button>
        <button
          onClick={() => handleSubmit('image/reconstruct')}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Reconstruct Image
        </button>
      </div>

      {loading && <p className="text-sm text-gray-500 mt-4">Processing...</p>}

      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded shadow text-sm">
          {result.error ? (
            <p className="text-red-600">{result.error}</p>
          ) : (
            <>
              <p className="text-green-700 font-medium">✅ {result.message}</p>
              {result.reconstruction_loss && (
                <p>
                  <strong>Reconstruction Loss:</strong>{' '}
                  {result.reconstruction_loss.toFixed(6)}
                </p>
              )}
              {result.avg_difference && (
                <p>
                  <strong>Average Pixel Change:</strong> {result.avg_difference.toFixed(6)}
                </p>
              )}
              {result.download_zip && (
                <a
                  href={`http://127.0.0.1:8000${result.download_zip}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block mt-2 text-blue-600 underline hover:text-blue-800"
                  download
                >
                  📦 Download ZIP (image + tensor)
                </a>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default ImageInference;
