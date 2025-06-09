import { useState, useEffect, useRef } from 'react';
// 修正：フックが返すオブジェクトの型もインポートします
import type { User, UseAttendanceSocketReturn } from '../types/attendance';

// 修正：フックの戻り値の型を更新します
export const useAttendanceSocket = (initialUsers: User[]): UseAttendanceSocketReturn => {
const [users, setUsers] = useState<User[]>(initialUsers);
// ▼▼▼ 修正点1: エラー状態を管理するstateを追加 ▼▼▼
const [error, setError] = useState<Error | null>(null);

const socketRef = useRef<WebSocket | null>(null);

useEffect(() => {
    if (!initialUsers) {
        return;
    }

    const basePath = process.env.REACT_APP_WEBSOCKET_BASE_PATH;
    const apiKey   = process.env.REACT_APP_WEBSOCKET_API_KEY;
    const stage    = 'v1';

    // ▼▼▼ 修正点2: 環境変数が未設定の場合もエラーとして扱う ▼▼▼
    if (!basePath || !apiKey) {
        const errorMessage = "WebSocketの接続に必要な環境変数(BASE_PATH or API_KEY)が設定されていません。";
        console.error(errorMessage);
        setError(new Error(errorMessage));
        return;
    }

    const fullUrl = `${basePath}/${stage}?apiKey=${apiKey}`;
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

    // ▼▼▼ 修正点3: onerrorイベントでエラー状態を更新 ▼▼▼
    socket.onerror = (event) => {
        console.error("WebSocketエラー:", event);
        setError(new Error("WebSocket接続で問題が発生しました。"));
    };

    // ▼▼▼ 修正点4: oncloseイベントで予期せぬ切断をエラーとして扱う ▼▼▼
    socket.onclose = (event) => {
        if (!event.wasClean) {
            console.error('WebSocket接続が予期せず切断されました。', event);
            setError(new Error(`サーバーとの接続が切れました。(コード: ${event.code})`));
        } else {
            console.log("WebSocket接続が正常に切断されました。");
        }
    };

    return () => {
        if (socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
    };
}, [initialUsers]);

// ▼▼▼ 修正点5: usersとerrorの両方を返す ▼▼▼
return { users, error };
};