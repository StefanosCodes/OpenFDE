import { Route, Routes } from "react-router-dom";

import { AgentOverviewPage } from "./pages/agent-overview";
import { AgentPaperPage } from "./pages/agent-paper";
import { AgentWorkspacePage } from "./pages/agent-workspace";
import { HomePage } from "./pages/home";
import { NotFoundPage } from "./pages/not-found";
import { StudioPaperPage } from "./pages/paper";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/paper" element={<StudioPaperPage />} />
      <Route path="/agents/:agentSlug" element={<AgentOverviewPage />} />
      <Route path="/agents/:agentSlug/paper" element={<AgentPaperPage />} />
      <Route path="/agents/:agentSlug/workspace" element={<AgentWorkspacePage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
