import { useState, useEffect } from 'react';

// 型定義 (変更なし)
type UserStatus = '在室' | '一時不在' | '退室';
interface User {
name: string;
status: UserStatus;
}

// カスタムフックが返す値の型定義 (変更なし)
interface UseGetAttendanceReturn {
users: User[] | null;
isLoading: boolean;
error: Error | null;
}

export const useGetAttendance = (): UseGetAttendanceReturn => {
const [users, setUsers] = useState<User[] | null>(null);
const [isLoading, setIsLoading] = useState<boolean>(true);
const [error, setError] = useState<Error | null>(null);

useEffect(() => {
    const fetchAttendance = async () => {
    try {
        const basePath = "https://q67wnmiw86.execute-api.ap-northeast-1.amazonaws.com";
        const url = `${basePath}/v1/attendance`;

        // ▼▼▼ 認証キーとヘッダー設定のコードをここから削除 ▼▼▼
        // const apiKey          = ...
        // const accessKey       = ...
        // const secretAccessKey = ...
        // const headers = new Headers();
        // ...
        // ▲▲▲ ここまで削除 ▲▲▲

        // ▼▼▼ fetchからheadersの指定を削除 ▼▼▼
        // GETリクエストなので、オプション指定も不要
        const response = await fetch(url);

        if (!response.ok) {
        throw new Error(`API response not OK: ${response.status}`);
        }

        const data = await response.json();
        const parsedBody = JSON.parse(data.body);

        setUsers(parsedBody);

    } catch (err) {
        console.error("Failed to fetch attendance:", err);
        if (err instanceof Error) {
            setError(err);
        } else {
            setError(new Error('An unknown error occurred'));
        }
    } finally {
        setIsLoading(false);
    }
    };

    fetchAttendance();
}, []);

return { users, isLoading, error };
};