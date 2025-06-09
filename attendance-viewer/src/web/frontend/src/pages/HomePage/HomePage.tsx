import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate }  from "react-router-dom";
import type { User, UserStatus }      from '../../types/attendance';
import { useAttendanceSocket } from '../../hooks/useAttendanceSocket';
import './HomePage.css';

// ユーザーの状態に応じた表示テキストとクラス名を取得する関数
const getStatusInfo = (status: UserStatus): { text: string; className: string } => {
    switch (status) {
        case 'clock_in':
        case 'break_out':
            return { text: '在室', className: 'present' };
        case 'break_in':
            return { text: '休憩中', className: 'away' };
        case 'clock_out':
            return { text: '退室', className: 'left' };
        default:
            return { text: '不明', className: 'unknown' };
    }
};

// 表示する列の定義
const STATUS_COLUMNS: ('在室' | '休憩中' | '退室')[] = ['在室', '休憩中', '退室'];

// ホームページコンポーネント
const HomePage: React.FC = () => {
    const location                      = useLocation();
    const navigate                      = useNavigate();
    const passedState                   = location.state as { users?: User[]; error?: string } | null;
    const [currentTime, setCurrentTime] = useState(new Date());

    // 初期状態として渡されたユーザー情報を取得
    const initialUsers = passedState?.users || [];
    // カスタムフックを使用してWebSocketからリアルタイムに更新されるユーザー情報を取得
    const users = useAttendanceSocket(initialUsers);

    // ページが読み込まれたときに、渡された状態がない場合はホームにリダイレクト
    useEffect(() => {
        if (!passedState) {
            navigate('/', { replace: true });
        }
        const timerId = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timerId);
    }, [passedState, navigate]);

    // ▼▼▼ 修正点：重複していた以下の行を削除 ▼▼▼
    // const users = passedState?.users || [];

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

// ▼▼▼ 修正点：HomePage.tsx内に不足していたヘルパー関数を追加 ▼▼▼
const mapApiStatusToDisplayStatus = (apiStatus: UserStatus): '在室' | '休憩中' | '退室' | null => {
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

const getStatusColorClass = (status: '在室' | '休憩中' | '退室'): string => {
    switch (status) {
        case '在室'  : return 'present';
        case '休憩中': return 'away';
        case '退室'  : return 'left';
    }
};

export default HomePage;