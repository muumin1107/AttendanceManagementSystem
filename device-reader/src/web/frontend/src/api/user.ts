const API_BASE = process.env.REACT_APP_API_BASE_URL;
const USER_ENDPOINT = `${API_BASE}/user`;

type UserData = {
	id: string;
	name: string;
};

export const postUser = async (data: UserData): Promise<boolean> => {
	if (!API_BASE) {
		console.error('API_BASE_URLが設定されていません');
		return false;
	}

	try {
		const res = await fetch(USER_ENDPOINT, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (!res.ok) {
			console.warn('ユーザー登録APIが失敗しました:', res.status);
			return false;
		}

		const contentType = res.headers.get('content-type');
		if (!contentType?.includes('application/json')) {
			console.warn('予期しないレスポンス形式:', await res.text());
			return false;
		}

		await res.json(); // 成功レスポンスの読み取り（使わなくてもパースで検証）
		return true;

	} catch (err: any) {
		console.error('ユーザー登録エラー:', err);
		return false;
	}
};
