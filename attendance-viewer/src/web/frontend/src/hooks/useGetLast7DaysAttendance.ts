import { useState, useEffect }                                 from 'react';
import type { Last7DaysData, UseGetLast7DaysAttendanceReturn } from '../types/attendance';

export const useGetLast7DaysAttendance = (): UseGetLast7DaysAttendanceReturn => {
    const [last7DaysData, setLast7DaysData] = useState<Last7DaysData>({});
    const [isLoading, setIsLoading]         = useState(true);
    const [error, setError]                 = useState<Error | null>(null);

    const getLast7Days = (): string[] => {
        const days = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            days.push(date.toISOString().split('T')[0]);
        }
        return days;
    };

    useEffect(() => {
        const fetchLast7DaysData = async () => {
            setIsLoading(true);
            setError(null);

            try {
                const last7Days = getLast7Days();
                const startDate = last7Days[0];
                const endDate   = last7Days[last7Days.length - 1];

                console.log('Fetching data for date range:', { startDate, endDate, last7Days });

                // APIエンドポイントを呼び出し（既存のsnapshotエンドポイントを使用）
                const response = await fetch(
                    `/api/attendance/snapshot?start_date=${startDate}&end_date=${endDate}`
                );

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const rawData = await response.json();
                console.log('Raw API response:', rawData);
                
                // データを過去7日間のみに絞り込み，時間形式に変換
                const processedData: Last7DaysData = {};
                
                Object.entries(rawData).forEach(([userName, userData]) => {
                    const userDailyData: { [date: string]: number } = {};
                    
                    last7Days.forEach(date => {
                        const dayData = (userData as any)[date];
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
                setLast7DaysData(processedData);
            } catch (err) {
                console.error('Error fetching last 7 days data:', err);
                setError(err instanceof Error ? err : new Error('Unknown error occurred'));
            } finally {
                setIsLoading(false);
            }
        };

        fetchLast7DaysData();
    }, []);

    return { last7DaysData, isLoading, error };
};