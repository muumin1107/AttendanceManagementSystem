import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const UserNameSelectPage = () => {
	const navigate = useNavigate();
	const [selectedName, setSelectedName] = useState('');

	const handleNextClick = () => {
		if (!selectedName) return;
		navigate('/register-user/waiting', {
			state: { name: selectedName }
		});
	};

	return (
		<div>
			<h2>ユーザー名を選択</h2>
			<select onChange={(e) => setSelectedName(e.target.value)} value={selectedName}>
				<option value="">-- 選択してください --</option>
				<option value="山田太郎">山田太郎</option>
				<option value="佐藤花子">佐藤花子</option>
			</select>
			<button onClick={handleNextClick} disabled={!selectedName}>
				次へ
			</button>
		</div>
	);
};

export default UserNameSelectPage;
