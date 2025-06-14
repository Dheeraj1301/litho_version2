import React, { useEffect, useState } from 'react';
import UploadCSV from './components/UploadCSV';
import InferenceForm from './components/InferenceForm';
import ImageInference from './components/ImageInference';
import AutoEncoderInfer from './components/AutoEncoderInfer';  // import this


function App() {
  const [serverStatus, setServerStatus] = useState("⏳ Checking server...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health/ping")
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "ok") {
          setServerStatus("✅ Server is up");
        } else {
          setServerStatus("❌ Server down");
        }
      })
      .catch(() => {
        setServerStatus("❌ Server down");
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded shadow-md">
        <h1 className="text-3xl font-bold mb-2 text-blue-700">🧠 Computational Lithography AI</h1>
        <p className="mb-4 text-sm text-gray-600">{serverStatus}</p>
        <UploadCSV />
        <InferenceForm />
        <ImageInference /> 
        <AutoEncoderInfer />
      </div>
    </div>
  );
}

export default App;
