import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import './HomePage.css';

// TypeScriptの型定義
type UserStatus = '在室' | '一時不在' | '退室';
interface User {
id: number;
name: string;
status: UserStatus;
}

// サンプルデータ
const mockUsers: User[] = [
{ id: 1, name: '山田 太郎', status: '在室' },
{ id: 2, name: '佐藤 花子', status: '一時不在' },
{ id: 3, name: '鈴木 一郎', status: '在室' },
{ id: 4, name: '高橋 次郎', status: '退室' },
{ id: 5, name: '田中 三郎', status: '在室' },
{ id: 6, name: '渡辺 四郎', status: '退室' },
{ id: 7, name: '伊藤 さくら', status: '一時不在' },
{ id: 8, name: '山本 五郎', status: '在室' },
];

// ▼▼▼ ヘルパー関数名を分かりやすく変更 ▼▼▼
// 状態に応じてCSSのカラークラス名を返すヘルパー関数
const getStatusColorClass = (status: UserStatus): string => {
switch (status) {
    case '在室': return 'present';
    case '一時不在': return 'away';
    case '退室': return 'left';
    default: return 'unknown';
}
};

// ▼▼▼ 表示するステータスの列を定義 ▼▼▼
const STATUS_COLUMNS: UserStatus[] = ['在室', '一時不在', '退室'];

// ホームページコンポーネント
const HomePage: React.FC = () => {
const [users, setUsers] = useState<User[]>(mockUsers);
const navigate = useNavigate();

useEffect(() => {
    const alreadyVisited = sessionStorage.getItem("hasVisited");
    if (!alreadyVisited) {
        sessionStorage.setItem("hasVisited", "true");
        navigate("/", { replace: true });
    }
}, [navigate]);

// ▼▼▼ 表示部分(return文)のテーブル構造を変更 ▼▼▼
return (
    <div className="attendance-board">
    <h1 className="board-title">在室状況一覧</h1>
    
    <div className="table-container">
        <table className="attendance-table">
        <thead>
            <tr>
            <th className="name-col">名前</th>
            {/* STATUS_COLUMNS配列からヘッダーを動的に生成 */}
            {STATUS_COLUMNS.map(status => (
                <th key={status} className="status-col">{status}</th>
            ))}
            </tr>
        </thead>
        <tbody>
            {users.map((user) => (
            <tr key={user.id}>
                <td>{user.name}</td>
                {/* STATUS_COLUMNSをループして各状態のセルを生成 */}
                {STATUS_COLUMNS.map(status => (
                <td key={status} className="status-cell">
                    {/* ユーザーの状態と列の状態が一致する場合のみマーカーを表示 */}
                    {user.status === status && (
                    <span className={`status-marker ${getStatusColorClass(status)}`}></span>
                    )}
                </td>
                ))}
            </tr>
            ))}
        </tbody>
        </table>
    </div>
    </div>
);
};

export default HomePage;