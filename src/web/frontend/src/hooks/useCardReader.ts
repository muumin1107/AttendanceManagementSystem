import { useEffect, useState, useRef } from 'react';
import { readCard } from '../api/cardReader';

// カードリーダーの読み取りを行うカスタムフック
export const useCardReader = () => {
	const [nfcId, setNfcId]         = useState<string | null>(null);
	const [isLoading, setIsLoading] = useState(true);
	const controllerRef             = useRef<AbortController | null>(null);

	useEffect(() => {
		const controller = new AbortController();
		controllerRef.current = controller;

		const fetchCard = async () => {
			const result = await readCard(controller.signal);
			if (result) {
				setNfcId(result);
			}
			setIsLoading(false);
		};

		fetchCard();

		return () => {
			// ページ離脱時の中断
			controller.abort();
		};
	}, []);

	const cancel = () => {
		controllerRef.current?.abort();
		setIsLoading(false);
	};

	return { nfcId, isLoading, cancel };
};
