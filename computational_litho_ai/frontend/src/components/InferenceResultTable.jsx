import React from "react";

function InferenceResultTable({ results }) {
  if (!results || results.length === 0) return null;

  const headers = Object.keys(results[0]);

  return (
    <div className="mt-4">
      <h2 className="text-lg font-semibold mb-2">Inference Results</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr>
              {headers.map((header) => (
                <th key={header} className="border px-4 py-2 bg-gray-100">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {results.map((row, idx) => (
              <tr key={idx}>
                {headers.map((key) => (
                  <td key={key} className="border px-4 py-2">
                    {row[key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default InferenceResultTable;
<button
  onClick={() => {
    const headers = Object.keys(results[0]);
    const csvContent = [
      headers.join(","),
      ...results.map((row) => headers.map((h) => row[h]).join(",")),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "inference_results.csv";
    link.click();
  }}
  className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
>
  Download CSV
</button>

