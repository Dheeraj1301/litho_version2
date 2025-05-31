import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = () => {
  const [params, setParams] = useState(["", "", "", ""]); // Customize length
  const [result, setResult] = useState(null);

  const handleChange = (index, value) => {
    const newParams = [...params];
    newParams[index] = value;
    setParams(newParams);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/predict', {
        parameters: params.map(parseFloat),
      });
      setResult(res.data.predicted_yield);
    } catch (err) {
      alert('Prediction failed: ' + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {params.map((val, i) => (
        <input
          key={i}
          type="number"
          value={val}
          onChange={(e) => handleChange(i, e.target.value)}
          placeholder={`Parameter ${i + 1}`}
          className="w-full p-2 border rounded"
          required
        />
      ))}
      <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        Predict Yield
      </button>
      {result !== null && (
        <div className="mt-4 text-green-700 font-semibold">
          Predicted Yield: {result}
        </div>
      )}
    </form>
  );
};

export default PredictionForm;
