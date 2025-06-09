import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import LoadingPage from './pages/LoadingPage/LoadingPage';
import ErrorPage from './pages/ErrorPage/ErrorPage';
import HomePage from './pages/HomePage/HomePage';

// アプリケーションのルーティングを定義するコンポーネント
function App() {
	return (
		<Router>
			<Routes>
				<Route path="/"      element={<LoadingPage />} />
				<Route path="/views" element={<HomePage />} />
				<Route path="/error"  element={<ErrorPage />} />
				<Route path="*"      element={<LoadingPage />} />
			</Routes>
		</Router>
	);
}

export default App;
