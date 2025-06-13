import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

function InferenceChart({ results }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">Prediction Chart</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={results}>
          <XAxis dataKey="wafer_id" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="prediction" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default InferenceChart;
