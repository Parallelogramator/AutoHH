import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import Matches from './pages/Matches';
import Profile from './pages/Profile';
import Docs from './pages/Docs';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Matches />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;