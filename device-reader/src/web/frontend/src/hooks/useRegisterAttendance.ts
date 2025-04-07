import { useState } from 'react';
import { postAttendance } from '../api/attendance';

export const useRegisterAttendance = () => {
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const submitAttendance = async (id: string, status: string): Promise<boolean> => {
		setIsSubmitting(true);
		setError(null);
		try {
			const success = await postAttendance({ id, status });
			if (!success) throw new Error('登録に失敗しました');
			return true;
		} catch (err) {
			setError((err as Error).message);
			return false;
		} finally {
			setIsSubmitting(false);
		}
	};

	return { isSubmitting, error, submitAttendance };
};
