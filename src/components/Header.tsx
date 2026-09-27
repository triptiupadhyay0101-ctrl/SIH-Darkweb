import {
  Search,
  Bell,
  ShieldCheck,
  Menu,
} from "lucide-react";

type HeaderProps = {
  onMenuClick: () => void;
};

function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-800 bg-slate-950/95 px-4 sm:px-6 backdrop-blur">

      {/* Left */}
      <div className="flex min-w-0 items-center gap-3">

        {/* Mobile Menu Button */}
        <button
          onClick={onMenuClick}
          className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white md:hidden"
          aria-label="Open navigation"
        >
          <Menu size={22} />
        </button>

        <div className="min-w-0">
          <p className="text-xs text-slate-500">
            Investigation Workspace
          </p>

          <h2 className="truncate text-sm font-semibold text-slate-200">
            <span className="text-blue-400">TraceX</span>{" "}
            Threat Intelligence Center
          </h2>
        </div>

      </div>

      {/* Right */}
      <div className="flex items-center gap-2 sm:gap-4">

        {/* Search */}
        <div className="relative hidden md:block">
          <Search
            size={17}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
          />

          <input
            type="text"
            placeholder="Search actor, handle, PGP, wallet..."
            className="h-9 w-72 rounded-lg border border-slate-800 bg-slate-900 pl-9 pr-4 text-sm text-slate-200 outline-none placeholder:text-slate-600 focus:border-blue-500"
          />
        </div>

        {/* Security Status */}
        <div className="hidden items-center gap-2 rounded-lg border border-emerald-900/50 bg-emerald-950/30 px-3 py-2 sm:flex">
          <ShieldCheck
            size={16}
            className="text-emerald-400"
          />

          <span className="text-xs text-emerald-400">
            System Secure
          </span>
        </div>

        {/* Notification */}
        <button
          className="relative rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white"
          aria-label="Notifications"
        >
          <Bell size={19} />

          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500" />
        </button>

        {/* Investigator Profile */}
        <div className="flex items-center gap-3 border-l border-slate-800 pl-2 sm:pl-4">

          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold">
            IA
          </div>

          <div className="hidden sm:block">
            <p className="text-sm font-medium text-slate-200">
              Investigator
            </p>

            <p className="text-xs text-slate-500">
              Analyst
            </p>
          </div>

        </div>

      </div>

    </header>
  );
}

export default Header;