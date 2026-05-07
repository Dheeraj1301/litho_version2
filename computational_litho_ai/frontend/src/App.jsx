import React, { useEffect, useState } from 'react';
import InferenceForm from './components/InferenceForm';
import ImageInference from './components/ImageInference';
import AutoEncoderInfer from './components/AutoEncoderInfer';
import ChatAssistant from './components/ChatAssistant';
import SectionErrorBoundary from './components/SectionErrorBoundary';

const features = [
  {
    title: 'CSV Yield Inference',
    description: 'Upload one CSV once, run prediction, inspect tabular output, and export results.',
  },
  {
    title: 'Model Inference',
    description: 'Run prediction and visualize tabular outputs with quick export support.',
  },
  {
    title: 'Image Workflows',
    description: 'Classify layouts and run AutoEncoder reconstruction in separate focused panels.',
  },
  {
    title: 'Data Assistant',
    description: 'Ask questions over uploaded/sample data and analyze generated tensor sessions.',
  },
];

function App() {
  const [serverStatus, setServerStatus] = useState('⏳ Checking server...');

  useEffect(() => {
    document.body.classList.add('app-mounted');

    return () => document.body.classList.remove('app-mounted');
  }, []);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health/ping')
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 'ok') {
          setServerStatus('✅ Server is up');
        } else {
          setServerStatus('❌ Server down');
        }
      })
      .catch(() => {
        setServerStatus('❌ Server down');
      });
  }, []);

  return (
    <div className="min-h-screen px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <header className="rounded-2xl border border-blue-100 bg-white/90 p-6 shadow-lg backdrop-blur sm:p-8">
          <p className="mb-3 inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-blue-700">
            Computational Lithography Platform
          </p>
          <h1 className="text-3xl font-black leading-tight text-slate-900 sm:text-4xl">
            🧠 Computational Lithography AI
          </h1>
          <p className="mt-3 max-w-3xl text-sm text-slate-600 sm:text-base">
            A unified workspace for production inference, image reconstruction workflows,
            and assistant-powered analysis over your uploaded data.
          </p>
          <p className="mt-4 text-sm font-medium text-slate-700">{serverStatus}</p>
        </header>

        <section className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <article
              key={feature.title}
              className="rounded-xl border border-slate-200/70 bg-white/90 p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <h2 className="text-sm font-bold text-slate-800">{feature.title}</h2>
              <p className="mt-1 text-xs leading-5 text-slate-600">{feature.description}</p>
            </article>
          ))}
        </section>

        <main className="mt-8 space-y-6">
          <SectionErrorBoundary title="CSV Inference">
            <InferenceForm />
          </SectionErrorBoundary>
          <SectionErrorBoundary title="Image Classification">
            <ImageInference />
          </SectionErrorBoundary>
          <SectionErrorBoundary title="AutoEncoder">
            <AutoEncoderInfer />
          </SectionErrorBoundary>
          <SectionErrorBoundary title="Data Assistant">
            <ChatAssistant />
          </SectionErrorBoundary>
        </main>
      </div>
    </div>
  );
}

export default App;
