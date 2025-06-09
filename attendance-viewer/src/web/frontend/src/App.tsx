import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import LoadingPage from './pages/LoadingPage/LoadingPage';
import HomePage from './pages/HomePage/HomePage';

// アプリケーションのルーティングを定義するコンポーネント
function App() {
	return (
		<Router>
			<Routes>
				<Route path="/"     element={<LoadingPage />} />
				<Route path="/views" element={<HomePage />} />
			</Routes>
		</Router>
	);
}

export default App;
