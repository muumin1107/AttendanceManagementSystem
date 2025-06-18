import { useState, useEffect, useRef } from 'react';
import type { User, FullUserInfo, UseAttendanceSocketReturn } from '../types/attendance';

export const useAttendanceSocket = (initialUsers: FullUserInfo[]): UseAttendanceSocketReturn => {
    const [users, setUsers] = useState<FullUserInfo[]>(initialUsers);
    const [error, setError] = useState<Error | null>(null);
    const socketRef = useRef<WebSocket | null>(null);
    const pingIntervalRef = useRef<NodeJS.Timeout | null>(null);

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

            // アイドルタイムアウトを防ぐために9分間隔でpingを送信
            pingIntervalRef.current = setInterval(() => {
                if (socket.readyState === WebSocket.OPEN) {
                    const pingTime = new Date().toLocaleString('ja-JP');
                    console.log(`Sending ping at: ${pingTime}`);
                    socket.send(JSON.stringify({ type: 'ping' }));
                }
            }, 9 * 60 * 1000); // 9分 = 540,000ミリ秒
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            // ping/pongメッセージの場合はログ出力のみ
            if (data.type === 'pong') {
                const pongTime = new Date().toLocaleString('ja-JP');
                console.log(`Received pong at: ${pongTime}`);
                return;
            }
            
            // 通常のユーザー情報更新
            const updatedUserInfo: User = data;
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
            
            // ping間隔をクリア
            if (pingIntervalRef.current) {
                clearInterval(pingIntervalRef.current);
                pingIntervalRef.current = null;
            }
            
            // 意図しない切断の場合にエラーを設定
            if (event.code !== 1000) { // 1000は正常な切断
                setError(new Error(`サーバーとの接続が切れました．コード: ${event.code}`));
            }
        };

        // コンポーネントのアンマウント時にWebSocket接続をクリーンに閉じる
        return () => {
            if (pingIntervalRef.current) {
                clearInterval(pingIntervalRef.current);
                pingIntervalRef.current = null;
            }
            if (socketRef.current) {
                socketRef.current.close(1000, "Component unmounted");
                socketRef.current = null;
            }
        };
    }, []); // 初回レンダリング時にのみ実行

    return { users, error };
};