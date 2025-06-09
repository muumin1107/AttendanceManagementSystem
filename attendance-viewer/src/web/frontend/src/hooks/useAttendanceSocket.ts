import { useState, useEffect, useRef } from 'react';
import type { User } from '../types/attendance';

export const useAttendanceSocket = (initialUsers: User[]): User[] => {
const [users, setUsers] = useState<User[]>(initialUsers);
const socketRef = useRef<WebSocket | null>(null);

useEffect(() => {
    if (!initialUsers) {
        return;
    }
    // ▼▼▼ 以下、接続ロジックを修正 ▼▼▼

    // 1. 環境変数からベースパスとAPIキーを読み込む
    const basePath = process.env.REACT_APP_WEBSOCKET_BASE_PATH;
    const apiKey = process.env.REACT_APP_WEBSOCKET_API_KEY;
    const stage = 'v1'; // ステージを定義

    // 2. 必要な環境変数が設定されているかチェック
    if (!basePath || !apiKey) {
        console.error("WebSocketの接続に必要な環境変数(BASE_PATH or API_KEY)が設定されていません。");
        return;
    }

    // 3. 認証情報を含む完全なURLを構築
    const fullUrl = `${basePath}/${stage}?apiKey=${apiKey}`;

    // 4. 新しいURLでWebSocketに接続
    const socket = new WebSocket(fullUrl);
    socketRef.current = socket;

    socket.onopen = () => {
        console.log(`WebSocketに接続しました: ${basePath}/${stage}`);
    };

    socket.onmessage = (event) => {
        const updatedUser: User = JSON.parse(event.data);
        console.log("WebSocketメッセージ受信:", updatedUser);

        setUsers(currentUsers =>
            currentUsers.map(user =>
                user.name === updatedUser.name ? { ...user, status: updatedUser.status } : user
            )
        );
    };

    socket.onerror = (error) => {
        console.error("WebSocketエラー:", error);
    };

    socket.onclose = () => {
        console.log("WebSocket接続が切断されました。");
    };

    return () => {
        if (socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
    };
}, [initialUsers]);

return users;
};