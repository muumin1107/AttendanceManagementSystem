import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserNameSelectPage.css';

// ユーザー名選択ページ（日本語＋英語）
const UserNameSelectPage = () => {
	const navigate = useNavigate();
	const [selectedName, setSelectedName] = useState('');

	// 環境変数から名前リストを取得
	const nameList = process.env.REACT_APP_USER_NAMES
		? process.env.REACT_APP_USER_NAMES.split(',')
		: [];

	const handleNextClick = () => {
		if (!selectedName) return;
		navigate('/register-user/waiting', {
			state: { name: selectedName }
		});
	};

	const handleCancel = () => {
		navigate('/');
	};

	return (
		<div id="user-name-select-page">
			<h2>
				ユーザー名を選択
				<br />
				<small>Select your name</small>
			</h2>

			<select onChange={(e) => setSelectedName(e.target.value)} value={selectedName}>
				<option value="">-- 選択してください / Please select --</option>
				{ nameList.map((name, index) => (
					<option key={index} value={name}>{name}</option>
				)) }
			</select>

			<div style={{ marginTop: '1rem' }}>
				<button onClick={handleNextClick} disabled={!selectedName}>
					次へ / Next
				</button>
			</div>

			<div style={{ marginTop: '1rem' }}>
				<button onClick={handleCancel}>
					中断 / Cancel
				</button>
			</div>
		</div>
	);
};

export default UserNameSelectPage;
