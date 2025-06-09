import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate }   from "react-router-dom";
import type { User, UserStatus }      from '../../types/attendance';
import './HomePage.css';

// 表示する列の定義
type DisplayStatus = '在室' | '休憩中' | '退室';
const STATUS_COLUMNS: DisplayStatus[] = ['在室', '休憩中', '退室'];

// APIから受け取ったstatusを，表示用のstatusに変換する関数
const mapApiStatusToDisplayStatus = (apiStatus: UserStatus): DisplayStatus | null => {
    switch (apiStatus) {
        case 'clock_in':
        case 'break_out':
            return '在室';
        case 'break_in':
            return '休憩中';
        case 'clock_out':
            return '退室';
        default:
            return null;
    }
};

// 表示用のstatusに応じてCSSクラス名を返す関数
const getStatusColorClass = (status: DisplayStatus): string => {
    switch (status) {
        case '在室'  : return 'present';
        case '休憩中': return 'away';
        case '退室'  : return 'left';
    }
};

// ホームページコンポーネント
const HomePage: React.FC = () => {
    const location                      = useLocation();
    const navigate                      = useNavigate();
    const passedState                   = location.state as { users?: User[]; error?: string } | null;
    const [currentTime, setCurrentTime] = useState(new Date());
    // ページが読み込まれたときに、渡された状態がない場合はホームにリダイレクト
    useEffect(() => {
        if (!passedState) {
            navigate('/', { replace: true });
        }
        const timerId = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timerId);
    }, [passedState, navigate]);
    // 渡された状態からユーザー情報を取得
    const users = passedState?.users || [];

    return (
        <div className="home-page-container">
            <header className="home-header">
                <h1 className="board-title">在室状況一覧</h1>
                <p className="current-time">
                    {currentTime.toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' })}&nbsp;
                    {currentTime.toLocaleTimeString('ja-JP')}
                </p>
            </header>
            <main className="table-container">
                <table className="attendance-table">
                    <thead>
                        <tr>
                            <th className="name-col">名前</th>
                            {STATUS_COLUMNS.map(colName => (
                                <th key={colName} className="status-col">{colName}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {users.length > 0 ? (
                            users.map((user) => {
                                // 各ユーザーの現在の表示ステータスを取得
                                const displayStatus = mapApiStatusToDisplayStatus(user.status);
                                return (
                                    <tr key={user.name}>
                                        <td>{user.name}</td>
                                        {STATUS_COLUMNS.map(colName => (
                                            <td key={colName} className="status-cell">
                                                {displayStatus === colName && (
                                                    <span className={`status-marker ${getStatusColorClass(colName)}`}></span>
                                                )}
                                            </td>
                                        ))}
                                    </tr>
                                );
                            })
                        ) : (
                            <tr>
                                <td colSpan={4} className="no-data-cell">表示するユーザーがいません．</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </main>
        </div>
    );
};

export default HomePage;