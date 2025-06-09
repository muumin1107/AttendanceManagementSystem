import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useCardReader } from '../../hooks/useCardReader';
import { useRegisterUser } from '../../hooks/useRegisterUser';
import './UserCardWaitPage.css';

// ユーザーのカードを待つページ（日本語＋英語）
const UserCardWaitPage = () => {
	const location = useLocation();
	const navigate = useNavigate();
	const name = location.state?.name;

	const { nfcId, isLoading, cancel } = useCardReader();
	const { submitUser, isSubmitting } = useRegisterUser();

	useEffect(() => {
		if (!nfcId || isSubmitting) return;

		const register = async () => {
			const success = await submitUser(nfcId, name);
			navigate('/', {
				state: {
					toast: success
						? 'ユーザー登録の受け付けに成功しました'
						: 'ユーザー登録の受け付けに失敗しました'
				}
			});
		};

		register();
	}, [nfcId]);

	const handleCancel = () => {
		cancel();
		navigate('/');
	};

	return (
		<div id="user-wait-page">

			<div className="card-animation">💳</div>

			<h2>
				カードをかざしてください
				<br />
				<small>Please hold your card over the reader</small>
			</h2>

			{isLoading ? (
				<p>
					カードを読み取っています...
					<br />
					<small>Reading card...</small>
				</p>
			) : nfcId ? (
				<p>&nbsp;</p>
			) : (
				<p>&nbsp;</p>
			)}

			<button onClick={handleCancel} id="cancel-button">
				中断 / Cancel
			</button>
		</div>
	);
};

export default UserCardWaitPage;
