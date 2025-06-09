import { useState, useEffect } from 'react';

// 型定義
type UserStatus = '在室' | '一時不在' | '退室';
interface User {
name: string;
status: UserStatus;
}

// カスタムフックが返す値の型定義
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

        const response = await fetch(url);

        if (!response.ok) {
        throw new Error(`API response not OK: ${response.status}`);
        }

        // ▼▼▼ 修正箇所 ▼▼▼
        // response.json()で既にデータがJavaScriptの配列に変換されている
        const data = await response.json(); 
        
        // 不要なJSON.parseを削除し、変換後のデータを直接セットする
        // const parsedBody = JSON.parse(data.body); // この行を削除
        setUsers(data); // dataを直接セット

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