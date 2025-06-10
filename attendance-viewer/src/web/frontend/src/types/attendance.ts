// ユーザーが取りうる状態
export type UserStatus = 'clock_in' | 'clock_out' | 'break_in' | 'break_out';
// ユーザーオブジェクトの型
export interface User {
    name  : string;
    status: UserStatus;
}
// ユーザー情報の型
export interface UserIdentifier {
    name : string;
    grade: string;
}
// useGetAttendanceフックが返す値の型
export interface UseGetAttendanceReturn {
    users    : User[] | null;
    isLoading: boolean;
    error    : Error | null;
}
// useGetUserフックが返す値の型
export interface UseGetUserReturn {
    users    : UserIdentifier[] | null;
    isLoading: boolean;
    error    : Error | null;
}
// useAttendanceSocketフックが返す値の型
export interface UseAttendanceSocketReturn {
    users: User[];
    error: Error | null;
}