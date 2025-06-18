import { useState, useEffect, useRef } from 'react';
import type { User, FullUserInfo, UseAttendanceSocketReturn } from '../types/attendance';

export const useAttendanceSocket = (initialUsers: FullUserInfo[]): UseAttendanceSocketReturn => {
    const [users, setUsers] = useState<FullUserInfo[]>(initialUsers);
    const [error, setError] = useState<Error | null>(null);
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        // WebSocketの接続URLを環境変数から取得
        const basePath = process.env.REACT_APP_WEBSOCKET_API_BASE_PATH;
        const stage = 'v1';

        if (!basePath) {
            const errorMessage = "WebSocketの接続URLが設定されていません．";
            setError(new Error(errorMessage));
            return;
        }

        const fullUrl = `${basePath}/${stage}/`;
        const socket = new WebSocket(fullUrl);
        socketRef.current = socket;

        socket.onopen = () => {
            const connectionTime = new Date().toLocaleString('ja-JP');
            console.log(`WebSocket connected at: ${connectionTime}`);
            setError(null);
        };

        socket.onmessage = (event) => {
            const updatedUserInfo: User = JSON.parse(event.data);
            setUsers(currentUsers =>
                currentUsers.map(user =>
                    user.name === updatedUserInfo.name
                        ? { ...user, status: updatedUserInfo.status }
                        : user
                )
            );
        };

        socket.onerror = (event) => {
            console.error("WebSocket Error:", event);
            setError(new Error("WebSocket接続で問題が発生しました．"));
        };

        socket.onclose = (event) => {
            const disconnectTime = new Date().toLocaleString('ja-JP');
            console.log(`WebSocket Closed at: ${disconnectTime}. Code: ${event.code}, Reason: ${event.reason}`);
            // 意図しない切断の場合にエラーを設定
            if (event.code !== 1000) { // 1000は正常な切断
                setError(new Error(`サーバーとの接続が切れました．コード: ${event.code}`));
            }
        };

        // コンポーネントのアンマウント時にWebSocket接続をクリーンに閉じる
        return () => {
            if (socketRef.current) {
                socketRef.current.close(1000, "Component unmounted");
                socketRef.current = null;
            }
        };
    }, []); // 初回レンダリング時にのみ実行

    return { users, error };
};