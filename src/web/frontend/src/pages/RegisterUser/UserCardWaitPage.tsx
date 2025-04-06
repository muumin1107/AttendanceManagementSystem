import { useLocation } from 'react-router-dom';

/**
 * カードをかざしてユーザー登録するページ
 */
const UserCardWaitPage = () => {
	const location = useLocation();
	const name = location.state?.name;

	return (
		<div>
			<h2>カードをかざしてください</h2>
			<p>登録するユーザー名：{name ?? '未指定'}</p>
		</div>
	);
};

export default UserCardWaitPage;
