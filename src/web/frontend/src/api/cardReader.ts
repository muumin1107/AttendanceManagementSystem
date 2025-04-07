const API_BASE = process.env.REACT_APP_API_BASE_URL;
const CARD_ENDPOINT = `${API_BASE}/card/read`;

type CardResponse = {
	nfc_id: string;
};

export const readCard = async (signal?: AbortSignal): Promise<string | null> => {
	if (!API_BASE) {
		console.error('API_BASE_URLが設定されていません');
		return null;
	}

	try {
		const res = await fetch(CARD_ENDPOINT, {
			method: 'GET',
			signal
		});

		if (!res.ok) {
			console.warn('カードAPIが失敗しました:', res.status);
			return null;
		}

		const contentType = res.headers.get('content-type');
		if (!contentType?.includes('application/json')) {
			console.warn('予期しないレスポンス形式:', await res.text());
			return null;
		}

		const data: CardResponse = await res.json();
		return data?.nfc_id ?? null;

	} catch (err: any) {
		if (err.name !== 'AbortError') {
			console.warn('カード読み取り中断または失敗:', err);
		}
		return null;
	}
};
