import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import './LoadingPage.css';

const LoadingPage = () => {
const navigate = useNavigate();

useEffect(() => {
    const alreadyVisited = sessionStorage.getItem("hasVisited");

    if (!alreadyVisited) {
    sessionStorage.setItem("hasVisited", "true");
    }

    // ここで必要な初期化処理を行う
    // 例えば、APIの呼び出しやデータの取得など

    // viewsページにリダイレクト
    navigate("/views", { replace: true });
}, [navigate]);

return (
    <div className="loading-container">
    <h1>読み込み中...</h1>
    <p>ページを準備しています</p>
    <div className="spinner" />
    </div>
);
};

export default LoadingPage;