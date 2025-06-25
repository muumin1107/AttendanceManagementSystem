import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuthenticator } from '@aws-amplify/ui-react';
import { useUpdateAttendanceAdmin } from '../../hooks/useUpdateAttendanceAdmin';
import type { UserStatus, UserIdentifier } from '../../types/attendance';
import './AdminPage.css';

const AdminPage = () => {
const { user, signOut } = useAuthenticator((context) => [context.user, context.signOut]);
const { updateAttendance, isLoading, error, isSuccess } = useUpdateAttendanceAdmin();

// HomePageから渡されたユーザーリストを取得します
const location = useLocation();
const allUsers = (location.state?.allUsers as UserIdentifier[]) || [];

// プルダウンで選択されたユーザー名とステータスを管理します
const [targetName, setTargetName] = useState<string>('');
const [targetStatus, setTargetStatus] = useState<UserStatus>('clock_in');

// ページ読み込み時に、プルダウンの初期値をリストの先頭ユーザーに設定します
useEffect(() => {
    if (allUsers.length > 0 && !targetName) {
    setTargetName(allUsers[0].name);
    }
}, [allUsers, targetName]);

const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!targetName) {
    alert('更新対象のユーザーを選択してください．');
    return;
    }
    updateAttendance(targetName, targetStatus);
};

return (
    <main className="admin-page-container">
    <header className="admin-header">
        <h1 className="admin-title">管理者ダッシュボード</h1>
        <button onClick={signOut} className="signout-button">サインアウト</button>
    </header>

    <p>ようこそ, {user?.signInDetails?.loginId || user?.username} さん</p>

    <div className="admin-contents">
        <form onSubmit={handleSubmit} className="update-form">
        <div className="form-group">
            <label htmlFor="name-select">ユーザー名</label>
            {/* テキスト入力の代わりにselect要素を使用します */}
            <select
            id="name-select"
            value={targetName}
            onChange={(e) => setTargetName(e.target.value)}
            required
            disabled={allUsers.length === 0}
            >
            {allUsers.length > 0 ? (
                allUsers.map((u) => (
                <option key={u.name} value={u.name}>
                    【{u.grade}】{u.name}
                </option>
                ))
            ) : (
                <option disabled>ユーザーリストがありません</option>
            )}
            </select>
        </div>
        <div className="form-group">
            <label htmlFor="status-select">新しいステータス</label>
            <select
            id="status-select"
            value={targetStatus}
            onChange={(e) => setTargetStatus(e.target.value as UserStatus)}
            >
            <option value="clock_in">🟢在室</option>
            <option value="break_in">🟡休憩中</option>
            {/* <option value="break_out">休憩終了</option> */}
            <option value="clock_out">⚫退室</option>
            </select>
        </div>
        <button type="submit" className="update-button" disabled={isLoading || allUsers.length === 0}>
            {isLoading ? '更新中...' : '在席情報を更新'}
        </button>
        </form>
        {isSuccess && <p className="success-message">更新に成功しました．</p>}
        {error && <p className="error-message">エラー: {error.message}</p>}
    </div>
    </main>
);
};

export default AdminPage;
