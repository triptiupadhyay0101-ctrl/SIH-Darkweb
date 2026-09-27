import { useNavigate, useLocation } from "react-router-dom";

import {
  LayoutDashboard,
  Search,
  User,
  Network,
  Clock3,
  Brain,
  FileDown,
  X,
} from "lucide-react";

const navigation = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    label: "Search",
    icon: Search,
    path: "/search",
  },
  {
    label: "Actor Profiles",
    icon: User,
    path: "/actor-profile",
  },
  {
    label: "Relationship Graph",
    icon: Network,
    path: "/relationship-graph",
  },
  {
    label: "Timeline",
    icon: Clock3,
    path: "/timeline",
  },
  {
    label: "AI Results",
    icon: Brain,
    path: "/ai-results",
  },
  {
    label: "Export",
    icon: FileDown,
    path: "/export",
  },
];

type SidebarProps = {
  mobileOpen: boolean;
  onClose: () => void;
};

function Sidebar({ mobileOpen, onClose }: SidebarProps) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path: string) => {
    navigate(path);
    onClose();
  };

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 z-50 flex h-screen w-64 flex-col border-r border-slate-800 bg-slate-950 transition-transform duration-300
        ${mobileOpen
            ? "translate-x-0"
            : "-translate-x-full"
          }
        md:translate-x-0`}
      >
        {/* TraceX Branding */}
        <div className="h-26 overflow-hidden border-b border-slate-800 px-4">
          <div className="flex h-full items-center justify-between">
            <img
              src="/tracex-logo.png"
              alt="TraceX - Threat Intelligence Platform"
              className="w-[330px] max-w-none -translate-x-14.5"
            />

            {/* Mobile close button */}
            <button
              onClick={onClose}
              className="absolute right-3 top-4 rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white md:hidden"
              aria-label="Close navigation"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-3 py-6">
          <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-widest text-slate-600">
            Investigation
          </p>

          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.path}
                onClick={() => handleNavigation(item.path)}
                className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition ${location.pathname === item.path
                    ? "bg-blue-500/10 text-blue-400"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white"
                  }`}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* System Status */}
        <div className="border-t border-slate-800 p-4">
          <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />

              <span className="text-xs font-medium text-slate-300">
                System Online
              </span>
            </div>

            <p className="mt-2 text-[11px] text-slate-600">
              Investigation environment active
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;