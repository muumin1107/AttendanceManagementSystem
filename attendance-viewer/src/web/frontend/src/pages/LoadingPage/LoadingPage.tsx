import { useEffect }        from "react";
import { useNavigate }      from "react-router-dom";
import { useGetAttendance } from "../../hooks/useGetAttendance";
import './LoadingPage.css';

const LoadingPage = () => {
    const navigate                    = useNavigate();
    const { users, isLoading, error } = useGetAttendance();

    useEffect(() => {
        // ローディング中は何もしない
        if (isLoading) {
            return;
        }
        // エラーが発生した場合，エラーページに遷移させる
        if (error) {
            console.error("Error fetching attendance data:", error);
            navigate("/error", {
                replace: true,
                state  : { message: error.message }
            });
            return;
        }
        // データが正常に取得できた場合，ホームページに遷移
        if (users) {
            navigate("/views", {
                replace: true,
                state  : { users: users }
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