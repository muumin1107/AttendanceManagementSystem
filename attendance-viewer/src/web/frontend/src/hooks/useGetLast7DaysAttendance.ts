import { useMemo } from 'react';
import type { Last7DaysData, UseGetLast7DaysAttendanceReturn } from '../types/attendance';
import { useGetSnapshot } from './useGetSnapshot';

export const useGetLast7DaysAttendance = (): UseGetLast7DaysAttendanceReturn => {
    // 過去7日間の日付配列を取得
    const last7Days = useMemo(() => {
        const days = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            days.push(date.toISOString().split('T')[0]);
        }
        return days;
    }, []);

    const startDate = last7Days[0];
    const endDate = last7Days[last7Days.length - 1];

    // useGetSnapshotを使用して過去7日間のデータを取得
    const { snapshotData, isLoading, error } = useGetSnapshot(startDate, endDate);

    // snapshotDataを過去7日間のみに絞り込み、時間形式に変換
    const last7DaysData = useMemo(() => {
        if (!snapshotData) return {};

        console.log('Processing snapshot data for last 7 days:', { startDate, endDate, last7Days });
        console.log('Raw snapshot data:', snapshotData);

        const processedData: Last7DaysData = {};

        Object.entries(snapshotData).forEach(([userName, userData]) => {
            const userDailyData: { [date: string]: number } = {};

            last7Days.forEach(date => {
                const dayData = userData[date];
                if (dayData && typeof dayData === 'number') {
                    // データが分単位の場合は時間に変換
                    userDailyData[date] = dayData / 60;
                } else {
                    userDailyData[date] = 0;
                }
            });

            processedData[userName] = userDailyData;
        });

        console.log('Processed last 7 days data:', processedData);
        return processedData;
    }, [snapshotData, last7Days]);

    return { last7DaysData, isLoading, error };
};