import React, { useEffect, useState } from 'react';
import './CurrentDateTime.css'; // CSSファイルのインポート

// CurrentDateTimeコンポーネントを定義
function CurrentDateTime() {
    // 現在の日時を保存するためのstateフックを定義
    const [dateTime, setDateTime] = useState(new Date());

    // useEffectでコンポーネントがマウントされた時に1秒ごとに日時を更新
    useEffect(() => {
        const timer = setInterval(() => setDateTime(new Date()), 1000);
        return () => clearInterval(timer); // コンポーネントがアンマウントされる際にタイマーをクリア
    }, []);

    // 日付をフォーマットする関数（日本のフォーマットで表示）
    const formatDate = (date) => {
        return date.toLocaleDateString('ja-JP', { year: 'numeric', month: '2-digit', day: '2-digit' });
    };

    // 時間をフォーマットする関数（日本のフォーマットで表示）
    const formatTime = (date) => {
        return date.toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    };

    // レンダリング部分（日時の表示）
    return (
        <div className="current-datetime">
            <div className="date">{formatDate(dateTime)}</div> {/* 日付表示 */}
            <div className="time">{formatTime(dateTime)}</div> {/* 時間表示 */}
        </div>
    );
}

export default CurrentDateTime; // モジュールをエクスポート