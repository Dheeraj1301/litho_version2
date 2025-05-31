import React from 'react';
import PredictionForm from '../components/PredictionForm';

const Home = () => {
  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4 text-center">Lithography Yield Predictor</h1>
      <PredictionForm />
    </div>
  );
};

export default Home;
