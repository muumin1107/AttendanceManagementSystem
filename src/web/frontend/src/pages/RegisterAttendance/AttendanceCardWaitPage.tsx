import { useLocation } from 'react-router-dom';

const AttendanceCardWaitPage = () => {
	const location = useLocation();
	const type = location.state?.type;

	return (
		<div>
			<h2>カードをかざしてください</h2>
			<p>打刻種別：{type ?? '未指定'}</p>
		</div>
	);
};

export default AttendanceCardWaitPage;
