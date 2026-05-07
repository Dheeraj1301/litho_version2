import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

const rootElement = document.getElementById('root');

function FrontendLoadError({ error }) {
  return (
    <div className="min-h-screen bg-slate-100 p-6 text-slate-900">
      <div className="mx-auto max-w-3xl rounded-2xl border border-red-200 bg-white p-6 shadow">
        <h1 className="text-2xl font-bold text-red-700">Frontend failed to load</h1>
        <p className="mt-3 text-sm text-slate-700">
          The React app shell loaded, but one of the app modules failed before the dashboard could render.
          Restart the Vite server and check the browser console for the full error.
        </p>
        <pre className="mt-4 overflow-x-auto rounded bg-red-50 p-4 text-xs text-red-800">
          {error?.message || String(error)}
        </pre>
      </div>
    </div>
  );
}

if (!rootElement) {
  throw new Error('Root element #root was not found in index.html');
}

const root = ReactDOM.createRoot(rootElement);

import('./App.jsx')
  .then(({ default: App }) => {
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  })
  .catch((error) => {
    console.error('Failed to load the React dashboard', error);
    root.render(<FrontendLoadError error={error} />);
  });
