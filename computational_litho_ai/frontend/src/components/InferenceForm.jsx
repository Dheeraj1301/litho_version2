import React, { useState } from 'react';
import axios from 'axios';

function InferenceForm() {
  const [response, setResponse] = useState(null);

  const handleInference = async () => {
    const dummyPayload = {
      pattern_id: 1,
      intensity: 0.88,
      linewidth_nm: 45,
      shape: "Circle",
      defect_type: "bridge"
    };

    try {
      const res = await axios.post("http://127.0.0.1:8000/inference/", dummyPayload);
      setResponse(res.data);
    } catch (err) {
      alert("❌ Inference failed");
      console.error(err);
    }
  };

  return (
    <div className="p-4">
      <button onClick={handleInference} className="bg-green-600 text-white px-3 py-1 rounded">Run Inference</button>
      {response && <pre className="mt-2 bg-gray-100 p-2 rounded">{JSON.stringify(response, null, 2)}</pre>}
    </div>
  );
}

export default InferenceForm;
