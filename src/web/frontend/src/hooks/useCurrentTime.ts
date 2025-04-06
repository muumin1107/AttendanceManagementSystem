import { useEffect, useState } from 'react';

// 曜日表示に使う定数（外に出すことで再利用性と明示性アップ）
const JAPANESE_WEEKDAYS = ['日', '月', '火', '水', '木', '金', '土'];

/**
 * 現在時刻を "YYYY年MM月DD日（曜） HH:MM:SS" の形式で1秒ごとに返すカスタムフック
 */
export const useCurrentTime = (): string => {
	const [formattedTime, setFormattedTime] = useState(() => formatDateTime(new Date()));

	useEffect(() => {
		const intervalId = setInterval(() => {
			const now = new Date();
			setFormattedTime(formatDateTime(now));
		}, 1000);

		return () => clearInterval(intervalId);
	}, []);

	return formattedTime;
};

/**
 * Dateオブジェクトを "YYYY年MM月DD日（曜） HH:MM:SS" の形式に整形する
 */
const formatDateTime = (date: Date): string => {
	const year    = date.getFullYear();
	const month   = String(date.getMonth() + 1).padStart(2, '0');
	const day 	  = String(date.getDate()).padStart(2, '0');
	const weekday = JAPANESE_WEEKDAYS[date.getDay()];

	const hours   = String(date.getHours()).padStart(2, '0');
	const minutes = String(date.getMinutes()).padStart(2, '0');
	const seconds = String(date.getSeconds()).padStart(2, '0');

	return `${year}年${month}月${day}日（${weekday}） ${hours}:${minutes}:${seconds}`;
};