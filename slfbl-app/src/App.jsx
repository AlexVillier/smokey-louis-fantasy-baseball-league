import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PointsPage from './pages/points-page';
import DefaultPage from './pages/default-page';
import PlayerPage from './pages/player-page';
import MatchupPage from './pages/matchup-page';
import './App.css'

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<DefaultPage />} />
          <Route path="/points" element={<PointsPage />} />
          <Route path="/players/:playerId" element={<PlayerPage />} />
          <Route path="/matchup" element={<MatchupPage />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
