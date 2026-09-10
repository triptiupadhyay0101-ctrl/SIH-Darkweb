import { BrowserRouter, Routes, Route } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";

import Welcome from "./components/ui/Welcome";

import Dashboard from "./pages/Dashboard";
import Search from "./pages/Search";
import ActorProfile from "./pages/ActorProfile";
import RelationshipGraph from "./pages/RelationshipGraph";
import Timeline from "./pages/Timeline";
import AIResults from "./pages/AIResults";
import Export from "./pages/Export";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Welcome Screen */}
        <Route path="/" element={<Welcome />} />
        <Route path="/welcome" element={<Welcome />} />

        {/* Dashboard Application */}
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/search" element={<Search />} />
          <Route path="/actor-profile" element={<ActorProfile />} />
          <Route path="/relationship-graph" element={<RelationshipGraph />} />
          <Route path="/timeline" element={<Timeline />} />
          <Route path="/ai-results" element={<AIResults />} />
          <Route path="/export" element={<Export />} />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;

