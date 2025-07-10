import React, { useEffect, useState } from 'react';
import UploadCSV from './components/UploadCSV';
import InferenceForm from './components/InferenceForm';
import ImageInference from './components/ImageInference';
import AutoEncoderInfer from './components/AutoEncoderInfer';
import ChatAssistant from './components/ChatAssistant'; // ✅ Import Chat Assistant

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
    <div className="p-8">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
        <h1 className="text-4xl font-extrabold mb-2 text-blue-700 text-center">🧠 Computational Lithography AI</h1>
        <p className="mb-6 text-sm text-gray-600 text-center">{serverStatus}</p>
        
        {/* Main features */}
        <UploadCSV />
        <InferenceForm />
        <ImageInference />
        <AutoEncoderInfer />

        {/* ✅ Chat Assistant Section */}
        <div className="mt-10">
          <ChatAssistant />
        </div>
      </div>
    </div>
  );
}

export default App;
