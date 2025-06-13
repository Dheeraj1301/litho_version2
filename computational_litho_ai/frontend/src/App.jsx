import React, { useEffect, useState } from 'react';
import UploadCSV from './components/UploadCSV';
import InferenceForm from './components/InferenceForm';

function App() {
  const [serverStatus, setServerStatus] = useState("⏳ Checking...");

  useEffect(() => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    fetch(`${backendUrl}/health/ping`)
      .then(res => res.json())
      .then(data => {
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
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Computational Lithography AI</h1>
      <div className="mb-4">{serverStatus}</div>
      <UploadCSV />
      <InferenceForm />
    </div>
  );
}

export default App;
