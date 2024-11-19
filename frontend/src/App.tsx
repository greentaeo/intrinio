// Path: /frontend/src/App.tsx

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ScreenerPage from './pages/Screener';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ScreenerPage />} />
      </Routes>
    </Router>
  );
}

export default App;