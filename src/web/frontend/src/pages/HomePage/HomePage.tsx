import { useNavigate } from 'react-router-dom';
import { useCurrentTime } from '../../hooks/useCurrentTime';
import './HomePage.css';

/**
 * ホーム画面コンポーネント
 * 勤怠操作とユーザー登録の入口
 */
const HomePage = () => {
	const navigate = useNavigate();
	const currentTime = useCurrentTime();

	/**
	 * 勤怠ボタンが押されたときの遷移処理
	 * @param type 勤怠種別（出勤 / 休入 / 休出 / 退勤）
	 */
	const handleAttendanceClick = (type: string) => {
		navigate('/register-attendance/waiting', { state: { type } });
	};

	/**
	 * ユーザー登録ボタンが押されたときの遷移処理
	 */
	const handleRegisterClick = () => {
		navigate('/register-user');
	};

	return (
		<div id="home-page">
			<div id="clock">{currentTime}</div>

			<div id="attendance-buttons">
				<button onClick={() => handleAttendanceClick('出勤')}>出勤</button>
				<button onClick={() => handleAttendanceClick('休入')}>休入</button>
				<button onClick={() => handleAttendanceClick('休出')}>休出</button>
				<button onClick={() => handleAttendanceClick('退勤')}>退勤</button>
			</div>

			<button onClick={handleRegisterClick} id="user-register-button">
				ユーザー登録
			</button>
		</div>
	);
};

export default HomePage;
