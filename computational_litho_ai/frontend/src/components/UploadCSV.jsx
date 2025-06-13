import React, { useState } from 'react';
import axios from 'axios';

function UploadCSV() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload/", formData);
      alert("✅ File uploaded successfully!");
    } catch (err) {
      alert("❌ Upload failed");
      console.error(err);
    }
  };

  return (
    <div className="p-4">
      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="ml-2 bg-blue-500 text-white px-3 py-1 rounded">Upload</button>
    </div>
  );
}

export default UploadCSV;
