const API_BASE = process.env.REACT_APP_API_BASE_URL;
const ATTENDANCE_ENDPOINT = `${API_BASE}/attendance`;

type AttendanceData = {
	id: string;
	status: string; // 出勤 / 退勤 / 休入 / 休出 など
};

export const postAttendance = async (data: AttendanceData): Promise<boolean> => {
	if (!API_BASE) {
		console.error('API_BASE_URLが設定されていません');
		return false;
	}

	try {
		const res = await fetch(ATTENDANCE_ENDPOINT, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (!res.ok) {
			console.warn('勤怠登録APIが失敗しました:', res.status);
			return false;
		}

		const contentType = res.headers.get('content-type');
		if (!contentType?.includes('application/json')) {
			console.warn('予期しないレスポンス形式:', await res.text());
			return false;
		}

		// 応答内容は使用しないが、バリデーションとして解析
		await res.json();
		return true;

	} catch (err: any) {
		console.error('勤怠登録エラー:', err);
		return false;
	}
};
