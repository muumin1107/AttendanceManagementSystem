import React, { useState, useEffect }      from 'react';
import { useLocation }                     from 'react-router-dom';
import { fetchAuthSession }                from '@aws-amplify/auth';
import { useAuthenticator }                from '@aws-amplify/ui-react';
import { useUpdateAttendanceAdmin }        from '../../hooks/useUpdateAttendanceAdmin';
import { useGetAttendanceSnapshot }        from '../../hooks/useGetAttendanceSnapshot';
import type { UserStatus, UserIdentifier } from '../../types/attendance';
import './AdminPage.css';

const AdminPage = () => {
    const { user, signOut }                                 = useAuthenticator((context) => [context.user, context.signOut]);
    const { updateAttendance, isLoading, error, isSuccess } = useUpdateAttendanceAdmin();
    const location                                          = useLocation();
    const [isAdmin, setIsAdmin]                             = useState<boolean>(false);
    const allUsers                                          = (location.state?.allUsers as UserIdentifier[]) || [];
    const [targetName, setTargetName]                       = useState<string>('');
    const [targetStatus, setTargetStatus]                   = useState<UserStatus>('clock_in');

    // スナップショットの取得
    const [startDate, setStartDate] = useState('2025-07-12');
    const [endDate, setEndDate]     = useState('2025-07-12');
    const {
        snapshotData,
        isLoading: isSnapshotLoading,
        error    : snapshotError,
    } = useGetAttendanceSnapshot(startDate, endDate);

    // 管理者かどうかを判定するためのuseEffect
    useEffect(() => {
        const checkAdminStatus = async () => {
        try {
            const session = await fetchAuthSession();
            const groups  = session.tokens?.idToken?.payload['cognito:groups'] as string[] || [];
            setIsAdmin(groups.includes('Admins'));
        } catch (e) {
            console.error("セッションの取得に失敗しました．", e);
            setIsAdmin(false);
        }
        };
        checkAdminStatus();
    }, []);

    // ユーザーリストが変更されたときに，初期値を設定するためのuseEffect
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

    const handleSnapshotTest = () => {
        console.log('--- スナップショット取得テスト ---');
        if (isSnapshotLoading) {
            console.log('読み込み中...');
            return;
        }
        if (snapshotError) {
            console.error('取得エラー:', snapshotError);
            return;
        }
        console.log('取得成功データ:', snapshotData);
    };

    return (
        <div className="admin-page-wrapper">
            <main className="admin-page-container">
                <header className="admin-header">
                    <h1 className="admin-title">管理者ページ</h1>
                    <button onClick={signOut} className="signout-button">サインアウト</button>
                </header>

                <p>ようこそ, {user?.signInDetails?.loginId || user?.username} さん</p>

                {isAdmin ? (
                    <div className="admin-contents">
                        <form onSubmit={handleSubmit} className="update-form">
                            <div className="form-group">
                                <label htmlFor="name-select">ユーザー名</label>
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
                                <select id="status-select" value={targetStatus} onChange={(e) => setTargetStatus(e.target.value as UserStatus)}>
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

                        <div className="test-section" style={{ marginTop: '32px', borderTop: '1px solid #ccc', paddingTop: '16px' }}>
                            <h2>開発用テスト</h2>
                            <p>
                                テスト範囲: {startDate} ~ {endDate}
                            </p>
                            <button type="button" onClick={handleSnapshotTest} className="test-button">
                                在室スナップショット取得テスト (コンソール確認)
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="admin-contents">
                        <p className="error-message">このページを閲覧する権限がありません．</p>
                    </div>
                )}
            </main>
        </div>
    );
};

export default AdminPage;
