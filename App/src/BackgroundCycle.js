import React, { useEffect, useState } from 'react';
import './BackgroundCycle.css'; // CSSファイルのインポート

const BackgroundCycle = () => {
    const [time, setTime] = useState(new Date()); // 現在の時刻を管理するstate
    const [backgroundClass, setBackgroundClass] = useState(''); // 背景クラスを管理するstate
    const [celestialBody, setCelestialBody] = useState('sun'); // 天体のクラス（太陽・月）を管理するstate

    // 毎秒時刻を更新するためのuseEffect
    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date()); // 現在の時刻を更新
        }, 1000);

        return () => clearInterval(timer); // コンポーネントがアンマウントされる際にタイマーをクリア
    }, []);

    // 背景と天体を時刻に基づいて更新するuseEffect
    useEffect(() => {
        const updateBackground = () => {
            const hours = time.getHours();
            const minutes = time.getMinutes();
            const totalMinutes = hours * 60 + minutes;

            // 背景と天体を時間帯に応じて切り替える
            let newBackgroundClass = '';
            let newCelestialBody = 'sun';

            if (totalMinutes >= 180 && totalMinutes < 540) { // 3:00 - 9:00 (朝)
                newBackgroundClass = 'morning';
                newCelestialBody = 'sun';
            } else if (totalMinutes >= 540 && totalMinutes < 900) { // 9:00 - 15:00 (昼)
                newBackgroundClass = 'day';
                newCelestialBody = 'sun';
            } else if (totalMinutes >= 900 && totalMinutes < 1260) { // 15:00 - 21:00 (夕方)
                newBackgroundClass = 'evening';
                newCelestialBody = 'moon';
            } else { // 21:00 - 3:00 (夜)
                newBackgroundClass = 'night';
                newCelestialBody = 'moon';
            }

            setBackgroundClass(newBackgroundClass); // 背景クラスを更新
            setCelestialBody(newCelestialBody); // 天体クラスを更新
        };

        updateBackground(); // 初期レンダリング時に呼び出す
        const intervalId = setInterval(updateBackground, 60000); // 毎分背景を更新

        return () => clearInterval(intervalId); // コンポーネントがアンマウントされる際にクリア
    }, [time]);

    return (
        <div className={`background ${backgroundClass}`}>
            <div 
                className={`celestial-body ${celestialBody}`} 
            ></div> {/* 天体を表示 */}
        </div>
    );
};

export default BackgroundCycle; // コンポーネントをエクスポート