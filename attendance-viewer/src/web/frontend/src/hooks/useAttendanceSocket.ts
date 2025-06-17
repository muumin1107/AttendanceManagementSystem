import { useState, useEffect, useRef, useCallback } from 'react';
import type { User, FullUserInfo, UseAttendanceSocketReturn } from '../types/attendance';

export const useAttendanceSocket = (initialUsers: FullUserInfo[]): UseAttendanceSocketReturn => {
    const [users, setUsers] = useState<FullUserInfo[]>(initialUsers);
    const [error, setError] = useState<Error | null>(null);
    const socketRef = useRef<WebSocket | null>(null);

    // ハートビート用のタイマーIDを保持
    const heartbeatTimerRef = useRef<NodeJS.Timeout | null>(null);
    const HEARTBEAT_INTERVAL_MS = 5 * 60 * 1000; // 5分 = 300000ミリ秒 (API Gatewayの10分より短く)

    // 再接続試行回数と最大試行回数
    const reconnectAttemptsRef = useRef<number>(0);
    const MAX_RECONNECT_ATTEMPTS = 10; // 最大再接続試行回数

    // WebSocketの接続関数を useCallback でメモ化
    const connectWebSocket = useCallback(() => {
        // 既存のソケットがあればクリーンアップして閉じる
        if (socketRef.current) {
            // クローズ処理をすることで、既存の onclose ハンドラが呼ばれるのを防ぐ
            // connectWebSocket自体が呼ばれた場合は、新しい接続を確立するため、
            // 既存の接続は「クリーンな切断」として扱いたい場合が多い
            // ただし、もし既存のoncloseで再接続ロジックをトリガーしたい場合はここを調整
            if (socketRef.current.readyState === WebSocket.OPEN || socketRef.current.readyState === WebSocket.CONNECTING) {
                socketRef.current.close(1000, "Initiating new connection attempt"); // クリーンなクローズコード1000
            }
            socketRef.current = null;
        }
        // 既存のハートビートタイマーがあればクリア
        if (heartbeatTimerRef.current) {
            clearInterval(heartbeatTimerRef.current);
            heartbeatTimerRef.current = null;
        }

        const basePath = process.env.REACT_APP_WEBSOCKET_API_BASE_PATH;
        const apiKey = process.env.REACT_APP_WEBSOCKET_API_KEY;
        const stage = 'v1';

        if (!basePath || !apiKey) {
            const errorMessage = "WebSocketの接続に必要な環境変数が設定されていません．";
            setError(new Error(errorMessage));
            return;
        }

        const fullUrl = `${basePath}/${stage}/?apiKey=${apiKey}`;
        const socket = new WebSocket(fullUrl);
        socketRef.current = socket;

        socket.onopen = () => {
            console.log("WebSocket connected.");
            setError(null); // 接続成功したらエラーをクリア
            reconnectAttemptsRef.current = 0; // 再接続成功したら試行回数をリセット

            // ハートビートを開始
            heartbeatTimerRef.current = setInterval(() => {
                if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
                    try {
                        socketRef.current.send(JSON.stringify({ action: "ping", timestamp: new Date().toISOString() }));
                        console.log('WebSocket: Sent heartbeat ping.');
                    } catch (e) {
                        console.error('Failed to send heartbeat:', e);
                    }
                }
            }, HEARTBEAT_INTERVAL_MS);
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
            // エラー時も再接続を試みる
            attemptReconnect();
        };

        const attemptReconnect = () => {
            if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
                const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000); // 1秒, 2秒, 4秒, ... 最大30秒
                console.log(`Attempting to reconnect in ${delay / 1000} seconds... (Attempt ${reconnectAttemptsRef.current + 1})`);
                reconnectAttemptsRef.current++;
                setTimeout(connectWebSocket, delay);
            } else {
                setError(new Error("WebSocketの再接続に失敗しました．ネットワークを確認してください．"));
                console.error("Failed to reconnect WebSocket after multiple attempts.");
            }
        };

        socket.onclose = (event) => {
            console.log(`WebSocket Closed. Code: ${event.code}, Reason: ${event.reason}, WasClean: ${event.wasClean}`);

            // ハートビートタイマーをクリア
            if (heartbeatTimerRef.current) {
                clearInterval(heartbeatTimerRef.current);
                heartbeatTimerRef.current = null;
            }

            // wasClean が false の場合、または特定のクローズコードの場合に再接続を試みる
            // 1000 (Normal Closure) 以外の切断の場合に再接続
            if (event.code !== 1000) {
                // `event.wasClean` が `true` であっても、
                // 1000 以外のコードであれば、意図しない切断と判断して再接続を試みる
                setError(new Error(`サーバーとの接続が切れました．コード: ${event.code}．理由: ${event.reason || '不明'}`));
                attemptReconnect();
            } else {
                // 1000 (Normal Closure) の場合は、エラーをクリアし、再接続はしない（意図的な切断と判断）
                setError(null);
                console.log("WebSocket connection closed cleanly.");
            }
        };
    }, []); // 依存配列が空なので、フックはマウント時に一度だけ作成される

    // useEffect のクリーンアップ関数: コンポーネントがアンマウントされるときにソケットを閉じる
    // connectWebSocket関数はuseCallbackでメモ化され、初回レンダリング時のみ実行されるため、
    // initialUsersの変更時に再接続をトリガーするなら、useEffectの依存配列に含めるか、
    // connectWebSocket内で再接続ロジックを完結させる必要があります。
    // 今回はconnectWebSocketが再接続を内部で管理するようにしています。
    useEffect(() => {
        connectWebSocket(); // コンポーネントマウント時にWebSocket接続を開始

        return () => {
            if (socketRef.current) {
                // クリーンアップ時には、クリーンなクローズコードでソケットを閉じる
                // これにより onclose で再接続がトリガーされるのを防ぐ
                socketRef.current.close(1000, "Component unmounted");
                socketRef.current = null;
            }
            if (heartbeatTimerRef.current) {
                clearInterval(heartbeatTimerRef.current);
                heartbeatTimerRef.current = null;
            }
        };
    }, [connectWebSocket]); // connectWebSocket は useCallback でメモ化されているため、初回レンダリング時のみ実行

    return { users, error };
};