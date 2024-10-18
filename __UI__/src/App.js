import './App.css';
import { useState } from 'react';

function App() {
  const [message, setMessage] = useState('クリックしてください');
  return (
    <div className="App">
      <header className="App-header">
        <p>{message}</p>
        <button onClick={() => setMessage('ボタンがクリックされました')}>
          クリック
        </button>
      </header>
    </div>
  );
}

export default App;
