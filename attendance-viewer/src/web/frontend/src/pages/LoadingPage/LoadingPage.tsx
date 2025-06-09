import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useGetAttendance } from "../../hooks/useGetAttendance";
import './LoadingPage.css';

const LoadingPage = () => {
    const navigate                        = useNavigate();
    const { users, isLoading, error }     = useGetAttendance();
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    useEffect(() => {
        // ローディング中は何もしない
        if (isLoading) {
            return;
        }
        // エラーが発生した場合はエラーメッセージを設定し、viewsに遷移
        if (error) {
            console.error(error);
            navigate("/views", {
                replace: true,
                state  : { error: "データの取得に失敗しました．"}
            });
            return;
        }
        // ユーザーデータが取得できた場合はviewsに遷移
        if (users) {
            navigate("/views", {
                replace: true,
                state  : {users: users}
            });
        }
    }, [isLoading, users, error, navigate]);

    return (
        <div className="loading-container">
        <h1>読み込み中...</h1>
        <p>ページを準備しています</p>
        <div className="spinner" />
        </div>
    );
};

export default LoadingPage;