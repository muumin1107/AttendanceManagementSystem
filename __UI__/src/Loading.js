import React from 'react';
import './Loading.css';

function Loading() {
    return (
        <div className="App">
        <header className="App-header">
            <div className="loading-container">
            <div className="loading-spinner"></div>
            <p className="loading-text-jp">読み込み中...</p>
            <p className="loading-text-en">Loading...</p>
            </div>
        </header>
        </div>
    );
}

export default Loading;