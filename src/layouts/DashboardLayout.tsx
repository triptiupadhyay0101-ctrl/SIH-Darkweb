import { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

function DashboardLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <Sidebar
        mobileOpen={mobileOpen}
        onClose={() => setMobileOpen(false)}
      />

      <div className="ml-0 min-w-0 md:ml-64">
        <Header onMenuClick={() => setMobileOpen(true)} />

        <main className="p-4 sm:p-6">
          <Outlet />
        </main>
      </div>

    </div>
  );
}

export default DashboardLayout;