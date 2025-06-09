import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import './HomePage.css';

// TypeScriptの型定義
// ユーザーが取りうる状態をリテラル型で定義
type UserStatus = '在室' | '一時不在' | '退室';

// ユーザーオブジェクトのインターフェースを定義
interface User {
id: number;
name: string;
status: UserStatus;
}

// APIの代わりとなるサンプルデータ（モックデータ）
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

// 状態に応じてCSSクラス名を返すヘルパー関数
const getStatusClass = (status: UserStatus): string => {
switch (status) {
    case '在室':
    return 'status-present';
    case '一時不在':
    return 'status-away';
    case '退室':
    return 'status-left';
    default:
    // 型定義により 'default' ケースは本来到達不能ですが，念のため記述
    return 'status-unknown';
}
};

// ホームページコンポーネント
const HomePage: React.FC = () => {
// useStateに型<User[]>を適用し，ユーザーリストを状態として管理
const [users, setUsers] = useState<User[]>(mockUsers);

const navigate = useNavigate();

useEffect(() => {
    const alreadyVisited = sessionStorage.getItem("hasVisited");

    if (!alreadyVisited) {
        sessionStorage.setItem("hasVisited", "true");
        // ページにリダイレクト
        navigate("/", { replace: true });
    }
}, [navigate]);

return (
    <div className="attendance-board">
    <h1 className="board-title">在室状況一覧</h1>
    <div className="user-grid">
        {/* users配列をmapで展開して，ユーザーカードを生成 */}
        {users.map((user) => (
        <div key={user.id} className="user-card">
            <div className="user-name">{user.name}</div>
            <div className={`status-badge ${getStatusClass(user.status)}`}>
            {user.status}
            </div>
        </div>
        ))}
    </div>
    </div>
);
};

export default HomePage;