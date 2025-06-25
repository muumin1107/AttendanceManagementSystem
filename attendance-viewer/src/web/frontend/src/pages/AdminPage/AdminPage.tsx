import React, { useState, useEffect } from 'react';
// Amplify Authライブラリから、認証情報を取得するための関数を直接インポートします
import { fetchAuthSession } from '@aws-amplify/auth';
import { useAuthenticator } from '@aws-amplify/ui-react';
import { useUpdateAttendanceAdmin } from '../../hooks/useUpdateAttendanceAdmin';
import type { UserStatus } from '../../types/attendance';
import './AdminPage.css';

const AdminPage = () => {
// `useAuthenticator`フックから必要な情報を取得します
const { user, signOut } = useAuthenticator((context) => [context.user, context.signOut]);
const { updateAttendance, isLoading, error, isSuccess } = useUpdateAttendanceAdmin();
const [isAdmin, setIsAdmin] = useState<boolean>(false);

const [targetName, setTargetName] = useState<string>('');
const [targetStatus, setTargetStatus] = useState<UserStatus>('clock_in');

useEffect(() => {
    const checkAdminStatus = async () => {
    try {
        // 現在の認証セッション（IDトークンなど）を取得します
        const session = await fetchAuthSession();
        // IDトークンのペイロードから、ユーザーが所属するグループの情報を取得します
        const groups = session.tokens?.idToken?.payload['cognito:groups'] as string[] || [];
        setIsAdmin(groups.includes('Admins'));
    } catch (e) {
        console.error("セッションの取得に失敗しました．", e);
        setIsAdmin(false);
    }
    };
    checkAdminStatus();
}, []);

const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!targetName.trim()) {
    alert('更新対象のユーザー名を入力してください．');
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

    {/* ユーザー情報は 'user.username' または 'user.signInDetails.loginId' から取得します */}
    <p>ようこそ, {user?.signInDetails?.loginId || user?.username} さん</p>

    {isAdmin ? (
        <div className="admin-contents">
        <form onSubmit={handleSubmit} className="update-form">
            <div className="form-group">
            <label htmlFor="name-input">ユーザー名</label>
            <input
                id="name-input"
                type="text"
                value={targetName}
                onChange={(e) => setTargetName(e.target.value)}
                placeholder="例: 佐藤 太郎"
                required
            />
            </div>
            <div className="form-group">
            <label htmlFor="status-select">新しいステータス</label>
            <select
                id="status-select"
                value={targetStatus}
                onChange={(e) => setTargetStatus(e.target.value as UserStatus)}
            >
                <option value="clock_in">出勤</option>
                <option value="clock_out">退勤</option>
                <option value="break_in">休憩開始</option>
                <option value="break_out">休憩終了</option>
            </select>
            </div>
            <button type="submit" className="update-button" disabled={isLoading}>
            {isLoading ? '更新中...' : '在席情報を更新'}
            </button>
        </form>
        {isSuccess && <p className="success-message">更新に成功しました．</p>}
        {error && <p className="error-message">エラー: {error.message}</p>}
        </div>
    ) : (
        <p className="error-message">このページを閲覧する権限がありません．</p>
    )}
    </main>
);
};

export default AdminPage;
