import { useState, useEffect, useRef }          from 'react';
import type { User, UseAttendanceSocketReturn } from '../types/attendance';

export const useAttendanceSocket = (initialUsers: User[]): UseAttendanceSocketReturn => {
    const [users, setUsers] = useState<User[]>(initialUsers);
    const [error, setError] = useState<Error | null>(null);
    const socketRef         = useRef<WebSocket | null>(null);

    useEffect(() => {
        // 初期ユーザーが設定されていない場合は何もしない
        if (!initialUsers) {
            return;
        }

        // WebSocketの接続設定
        const basePath = process.env.REACT_APP_WEBSOCKET_API_BASE_PATH;
        const apiKey   = process.env.REACT_APP_WEBSOCKET_API_KEY;
        const stage    = 'v1';
        // 必要な環境変数が設定されているか確認
        if (!basePath || !apiKey) {
            const errorMessage = "WebSocketの接続に必要な環境変数が設定されていません．";
            setError(new Error(errorMessage));
            return;
        }
        // WebSocketのURLを構築
        const fullUrl = `${basePath}/${stage}/?apiKey=${apiKey}`;
        const socket  = new WebSocket(fullUrl);
        socketRef.current = socket;

        // WebSocketの接続が開かれたときの処理
        socket.onopen = () => {};
        // メッセージ受信時の処理
        socket.onmessage = (event) => {
            const updatedUser: User = JSON.parse(event.data);
            setUsers(currentUsers =>
                currentUsers.map(user =>
                    user.name === updatedUser.name ? { ...user, status: updatedUser.status } : user
                )
            );
        };
        // エラー処理
        socket.onerror = (event) => {
            setError(new Error("WebSocket接続で問題が発生しました．"));
        };
        // 接続が閉じられたときの処理
        socket.onclose = (event) => {
            if (!event.wasClean) {
                setError(new Error(`サーバーとの接続が切れました: ${event.code}`));
            }
        };
        // クリーンアップ関数
        return () => {
            if (socket.readyState === WebSocket.OPEN) {
                socket.close();
            }
        };
    }, [initialUsers]);

    return { users, error };
};