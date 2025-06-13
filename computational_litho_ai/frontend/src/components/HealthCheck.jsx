import React, { useEffect, useState } from 'react';
import axios from 'axios';

function HealthCheck() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/health/ping")
      .then(res => setStatus(res.data.message))
      .catch(() => setStatus("❌ Server down"));
  }, []);

  return <p className="text-sm text-gray-600">Backend Status: {status}</p>;
}

export default HealthCheck;
