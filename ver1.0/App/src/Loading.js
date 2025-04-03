import React from 'react';
import './Loading.css'; // CSSファイルのインポート

// Loadingコンポーネントを定義
function Loading() {
    return (
        <div className="Loading">
            <header className="Loading-header">
                <div className="loading-container"> {/* ローディング要素を中央に配置 */}
                    <div className="loading-spinner"></div> {/* スピナー表示 */}
                    <p className="loading-text-jp">読み込み中...</p> {/* 日本語のローディングテキスト */}
                    <p className="loading-text-en">Loading...</p> {/* 英語のローディングテキスト */}
                </div>
            </header>
        </div>
    );
}

export default Loading; // コンポーネントをエクスポート