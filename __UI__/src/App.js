import React, { useState } from 'react';
import CurrentDateTime from './CurrentDateTime';
import CardReading from './CardReading';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const handleStartLoading = () => {setIsLoading(true);};

  if (isLoading) {
    return <CardReading />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <CurrentDateTime />
        <button className="start-button" onClick={handleStartLoading}>Start Loading</button>
      </header>
    </div>
  );
}

export default App;