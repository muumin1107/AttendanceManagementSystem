import { useNavigate, useLocation } from 'react-router-dom';
import { useCurrentTime } from '../../hooks/useCurrentTime';
import { useEffect, useState } from 'react';
import './HomePage.css';

const statusMap: Record<string, string> = {
	'出勤': 'clock_in',
	'休入': 'break_in',
	'休出': 'break_out',
	'退勤': 'clock_out'
};

const HomePage = () => {
	const navigate = useNavigate();
	const location = useLocation();
	const { date, time } = useCurrentTime();

	const [toast, setToast] = useState<string | null>(null);

	useEffect(() => {
		if (location.state?.toast) {
			setToast(location.state.toast);
			const timer = setTimeout(() => setToast(null), 3000);
			return () => clearTimeout(timer);
		}
	}, [location.state]);

	const handleAttendanceClick = (label: string) => {
		const status = statusMap[label];
		navigate('/register-attendance/waiting', { state: { type: status } });
	};

	const handleRegisterClick = () => {
		navigate('/register-user');
	};

	return (
		<div id="home-page">
			{/* トースト表示 */}
			{toast && <div className="toast">{toast}</div>}

			<div id="clock">
				<div className="clock-date">{date}</div>
				<div className="clock-time">{time}</div>
			</div>

			<div id="attendance-buttons">
				<button onClick={() => handleAttendanceClick('出勤')}>
					出勤<br /><small>Clock In</small>
				</button>
				<button onClick={() => handleAttendanceClick('休入')}>
					休入<br /><small>Break Start</small>
				</button>
				<button onClick={() => handleAttendanceClick('休出')}>
					休出<br /><small>Break End</small>
				</button>
				<button onClick={() => handleAttendanceClick('退勤')}>
					退勤<br /><small>Clock Out</small>
				</button>
			</div>

			<button onClick={handleRegisterClick} id="user-register-button">
				ユーザー登録<br /><small>User Registration</small>
			</button>
		</div>
	);
};

export default HomePage;
