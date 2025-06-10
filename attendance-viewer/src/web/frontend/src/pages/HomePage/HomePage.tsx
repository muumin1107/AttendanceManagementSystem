import React, { useState, useEffect }            from 'react';
import { useLocation, useNavigate }              from "react-router-dom";
import type { User, UserStatus, UserIdentifier } from '../../types/attendance';
import { useAttendanceSocket }                   from '../../hooks/useAttendanceSocket';
import './HomePage.css';

// 在室状況の列名を定義
const STATUS_COLUMNS: ('在室' | '休憩中' | '退室')[] = ['在室', '休憩中', '退室'];

// APIからのユーザーステータスを表示用のステータスに変換する関数
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

// ステータスに応じた色のクラス名を取得する関数
const getStatusColorClass = (status: '在室' | '休憩中' | '退室'): string => {
    switch (status) {
        case '在室'  : return 'present';
        case '休憩中': return 'away';
        case '退室'  : return 'left';
        default:
            return 'unknown';
    }
};

// ホームページコンポーネント
const HomePage: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();

    // URLの状態からattendanceUsersとallUsersを取得
    const passedState = location.state as {
        attendanceUsers?: User[];
        allUsers?: UserIdentifier[];
    } | null;

    const [currentTime, setCurrentTime] = useState(new Date());

    // 初期の在室ユーザーリストを取得
    const initialUsers = passedState?.attendanceUsers || [];

    // useAttendanceSocketフックを使用してWebSocket接続を確立し、リアルタイムの在室状況を取得
    const { users, error: socketError } = useAttendanceSocket(initialUsers);

    // ページが読み込まれたときに、URLの状態が存在しない場合はホームページにリダイレクト
    useEffect(() => {
        if (!passedState) {
            navigate('/', { replace: true });
        }
        const timerId = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timerId);
    }, [passedState, navigate]);

    // WebSocket接続エラーが発生した場合、エラーページにリダイレクト
    useEffect(() => {
        if (socketError) {
            navigate('/error', {
                replace: true,
                state: { message: `リアルタイム接続エラー: ${socketError.message}` }
            });
        }
    }, [socketError, navigate]);

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

export default HomePage;