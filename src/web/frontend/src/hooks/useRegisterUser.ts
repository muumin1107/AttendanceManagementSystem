import { useState } from 'react';
import { postUser } from '../api/user';

export const useRegisterUser = () => {
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const submitUser = async (id: string, name: string): Promise<boolean> => {
		setIsSubmitting(true);
		setError(null);
		try {
			const success = await postUser({ id, name });
			if (!success) throw new Error('登録に失敗しました');
			return true;
		} catch (err) {
			setError((err as Error).message);
			return false;
		} finally {
			setIsSubmitting(false);
		}
	};

	return { isSubmitting, error, submitUser };
};
