import { Routes, Route } from 'react-router';
import { RootLayout } from './components/layout/RootLayout';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { HomePlaceholder } from './pages/HomePlaceholder';
import { NotFound } from './pages/NotFound';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Profile } from './pages/Profile';
import { DatasetCatalog } from './pages/datasets/DatasetCatalog';
import { DatasetUpload } from './pages/datasets/DatasetUpload';
import { DatasetDetails } from './pages/datasets/DatasetDetails';
import { DatasetProfile } from './pages/processing/DatasetProfile';
import AnalyticsOverview from './pages/analytics/AnalyticsOverview';
import AIChatPage from './pages/AI/AIChatPage';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<RootLayout />}>
          <Route index element={<HomePlaceholder />} />
          <Route path="profile" element={<Profile />} />
          <Route path="datasets" element={<DatasetCatalog />} />
          <Route path="datasets/upload" element={<DatasetUpload />} />
          <Route path="datasets/:id" element={<DatasetDetails />} />
          <Route path="datasets/:id/profile" element={<DatasetProfile />} />
          <Route path="datasets/:id/analytics" element={<AnalyticsOverview />} />
          <Route path="ai/chat" element={<AIChatPage />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
