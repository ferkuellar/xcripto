import { HashRouter, Route, Routes } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'
import CommandCenter from '@/pages/CommandCenter'
import NewsIntake from '@/pages/NewsIntake'
import SourceValidation from '@/pages/SourceValidation'
import RiskReviewPage from '@/pages/RiskReviewPage'
import EditorialDesk from '@/pages/EditorialDesk'
import AgentsPage from '@/pages/AgentsPage'
import KnowledgeGraphPage from '@/pages/KnowledgeGraphPage'
import AuditPage from '@/pages/AuditPage'
import MetricsPage from '@/pages/MetricsPage'
import {
  CalendarPage,
  DistributionPage,
  MarketImpactPage,
  MemoryPage,
  ScriptsPage,
  SettingsPage,
  SocialClipsPage,
} from '@/pages/SecondaryPages'

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<CommandCenter />} />
          <Route path="/intake" element={<NewsIntake />} />
          <Route path="/sources" element={<SourceValidation />} />
          <Route path="/impact" element={<MarketImpactPage />} />
          <Route path="/risk" element={<RiskReviewPage />} />
          <Route path="/editorial" element={<EditorialDesk />} />
          <Route path="/scripts" element={<ScriptsPage />} />
          <Route path="/clips" element={<SocialClipsPage />} />
          <Route path="/distribution" element={<DistributionPage />} />
          <Route path="/calendar" element={<CalendarPage />} />
          <Route path="/metrics" element={<MetricsPage />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/graph" element={<KnowledgeGraphPage />} />
          <Route path="/memory" element={<MemoryPage />} />
          <Route path="/audit" element={<AuditPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </HashRouter>
  )
}

export default App
