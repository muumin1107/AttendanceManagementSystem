import React from 'react';
import { useLocation } from "react-router-dom";
// import './HomePage.css';

const HomePage: React.FC = () => {
    // useLocationフックを使って現在のURLのlocationオブジェクトを取得します
    const location = useLocation();
    const receivedState = location.state;

    return (
        <div className="home-container">
        <h1 className="home-title">HomePage</h1>
        <p>前のページから渡されたデータ（state）の中身です。</p>

        <div className="data-container">
            <h2 className="data-title">受信データ</h2>
            {receivedState ? (
            // 受け取ったstateオブジェクトをJSON形式の文字列に変換して表示します
            // null, 2 を指定することで、見やすくインデントされます
            <pre>{JSON.stringify(receivedState, null, 2)}</pre>
            ) : (
            // 直接/viewにアクセスした場合など、stateが存在しない場合のメッセージ
            <p>データが渡されませんでした。ローディングページから遷移してください。</p>
            )}
        </div>
        </div>
    );
};

export default HomePage;