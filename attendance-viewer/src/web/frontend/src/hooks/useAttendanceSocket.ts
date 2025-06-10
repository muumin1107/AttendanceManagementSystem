import { useState, useEffect, useRef }                        from 'react';
import type { User, FullUserInfo, UseAttendanceSocketReturn } from '../types/attendance';

export const useAttendanceSocket = (initialUsers: FullUserInfo[]): UseAttendanceSocketReturn => {
    const [users, setUsers] = useState<FullUserInfo[]>(initialUsers);
    const [error, setError] = useState<Error | null>(null);
    const socketRef         = useRef<WebSocket | null>(null);

    useEffect(() => {
        // WebSocketの接続を初期化
        const basePath = process.env.REACT_APP_WEBSOCKET_API_BASE_PATH;
        const apiKey   = process.env.REACT_APP_WEBSOCKET_API_KEY;
        const stage    = 'v1';
        // 環境変数が設定されていない場合はエラーをセット
        if (!basePath || !apiKey) {
            const errorMessage = "WebSocketの接続に必要な環境変数が設定されていません．";
            setError(new Error(errorMessage));
            return;
        }

        const fullUrl = `${basePath}/${stage}/?apiKey=${apiKey}`;
        const socket  = new WebSocket(fullUrl);
        socketRef.current = socket;

        socket.onopen = () => {};

        socket.onmessage = (event) => {
        // WebSocketからのメッセージは{name, status}のUser型
        const updatedUserInfo: User = JSON.parse(event.data);
        // 受信したユーザー情報をもとに、現在のユーザーリストを更新
        setUsers(currentUsers =>
            currentUsers.map(user =>
            // ユーザー名が一致する場合はステータスを更新
            user.name === updatedUserInfo.name
                ? { ...user, status: updatedUserInfo.status }
                : user
            )
        );
        };
        // WebSocketのエラー処理
        socket.onerror = (event) => {
            setError(new Error("WebSocket接続で問題が発生しました。"));
        };
        // WebSocketの接続が閉じられたときの処理
        socket.onclose = (event) => {
            if (!event.wasClean) {
                setError(new Error(`サーバーとの接続が切れました: ${event.code}`));
            }
        };

        return () => {
            if (socket.readyState === WebSocket.OPEN) {
                socket.close();
            }
        };
    }, [initialUsers]);

    return { users, error };
};