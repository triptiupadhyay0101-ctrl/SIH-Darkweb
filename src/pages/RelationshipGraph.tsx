import {
  User,
  AtSign,
  KeyRound,
  Wallet,
  Globe,
  Network,
  Search,
  ZoomIn,
  ZoomOut,
  Maximize2,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
function RelationshipGraph() {
  const [loading, setLoading] = useState(true);
  const graphRef = useRef<HTMLDivElement>(null);
  const [zoom, setZoom] = useState(1);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-2 border-slate-700 border-t-blue-500" />

          <p className="mt-4 text-sm font-medium text-slate-300">
            Loading relationship graph...
          </p>

          <p className="mt-1 text-xs text-slate-600">
            Mapping connected entities
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">

        <div>
          <p className="text-sm font-medium uppercase tracking-wider text-blue-400">
            INVESTIGATION / RELATIONSHIPS
          </p>

          <h1 className="mt-2 text-3xl font-semibold text-white">
            Relationship Graph
          </h1>

          <p className="mt-2 max-w-2xl text-sm text-slate-400">
            Visualize relationships between threat actors, identities,
            cryptographic indicators and infrastructure.
          </p>
        </div>

        <div className="flex items-center gap-2">

          <button
            onClick={() => setZoom((current) => Math.min(current + 0.1, 1.5))}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900 text-slate-400 transition hover:text-white"
            title="Zoom in"
          >
            <ZoomIn size={17} />
          </button>

          <button
            onClick={() => setZoom((current) => Math.max(current - 0.1, 0.8))}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900 text-slate-400 transition hover:text-white"
            title="Zoom out"
          >
            <ZoomOut size={17} />
          </button>

          <button
            onClick={() => graphRef.current?.requestFullscreen()}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900 text-slate-400 transition hover:text-white"
          >

            <Maximize2 size={16} />
          </button>

        </div>

      </div>


      {/* Search */}
      <div className="flex flex-col gap-3 rounded-xl border border-slate-800 bg-slate-900 p-4 md:flex-row">

        <div className="relative flex-1">

          <Search
            size={17}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
          />

          <input
            type="text"
            placeholder="Search actor, handle, wallet, PGP key or domain..."
            className="w-full rounded-lg border border-slate-800 bg-slate-950 py-2.5 pl-10 pr-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-blue-500/50"
          />

        </div>

        <button className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-500">
          Analyze
        </button>

      </div>


      {/* Graph */}
      <div className="grid gap-5 xl:grid-cols-[1fr_280px]">

        <div
          ref={graphRef}
          className="relative min-h-[650px] overflow-auto rounded-xl border border-slate-800 bg-slate-950"
        >          <div
          className="absolute inset-0 min-w-[700px] transition-transform duration-200"
          style={{
            transform: `scale(${zoom})`,
            transformOrigin: "center",
          }}
        >
            {/* Grid background */}
            <div
              className="absolute inset-0 opacity-30"
              style={{
                backgroundImage:
                  "linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(90deg, #1e293b 1px, transparent 1px)",
                backgroundSize: "40px 40px",
              }}
            />

            {/* Connection Lines */}
            <div className="absolute left-1/2 top-[33%] h-px w-[22%] -translate-x-full bg-slate-700" />

            <span className="absolute left-[32%] top-[30%] z-20 rounded bg-slate-950 px-1 text-[10px] font-medium text-slate-500">
              uses
            </span>
            <div className="absolute left-1/2 top-[33%] h-[17%] w-px bg-slate-700" />

            <span className="absolute left-[51%] top-[38%] z-20 -translate-x-1/2 rounded bg-slate-950 px-1 text-[10px] font-medium text-slate-500">
              identified by
            </span>

            <div className="absolute left-[50%] top-[33%] h-px w-[22%] bg-slate-700" />

            <span className="absolute left-[68%] top-[30%] z-20 rounded bg-slate-950 px-1 text-[10px] font-medium text-slate-500">
              linked to
            </span>

            <div className="absolute left-[28%] top-[50%] h-px w-[22%] bg-slate-700" />

            <div className="absolute left-[50%] top-[50%] h-px w-[22%] bg-slate-700" />

            <div className="absolute left-1/2 top-[50%] h-[17%] w-px bg-slate-700" />

            <span className="absolute left-[51%] top-[57%] -translate-x-1/2 text-[10px] font-medium text-slate-500">
              hosted on
            </span>

            <div className="absolute left-[72%] top-[50%] h-[17%] w-px bg-slate-700" />

            {/* Actor */}
            <GraphNode
              icon={User}
              title="ShadowFox"
              subtitle="Threat Actor"
              position="absolute left-1/2 top-[20%] -translate-x-1/2"
              active
            />

            {/* Handle */}
            <GraphNode
              icon={AtSign}
              title="@shadow_47"
              subtitle="Handle"
              position="absolute left-[16%] top-[42%]"
            />

            {/* PGP */}
            <GraphNode
              icon={KeyRound}
              title="PGP Key"
              subtitle="8A42...4F28"
              position="absolute left-1/2 top-[42%] -translate-x-1/2"
            />

            {/* Wallet */}
            <GraphNode
              icon={Wallet}
              title="0x7A91...C42F"
              subtitle="Crypto Wallet"
              position="absolute right-[16%] top-[42%]"
            />

            {/* Platform */}
            <GraphNode
              icon={Globe}
              title="Underground Forum"
              subtitle="Platform"
              position="absolute left-1/2 top-[67%] -translate-x-1/2"
            />

            {/* Secondary platform */}
            <GraphNode
              icon={Globe}
              title="Marketplace"
              subtitle="Platform"
              position="absolute left-[16%] top-[67%]"
            />

            {/* Onion Service */}
            <GraphNode
              icon={Globe}
              title="darkfox7x...onion"
              subtitle="Onion Service"
              position="absolute right-[16%] top-[67%]"
            />
          </div>

          {/* Status */}
          <div className="absolute bottom-4 left-4 flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-900/90 px-3 py-2">

            <Network size={15} className="text-blue-400" />

            <span className="text-xs text-slate-400">
              7 entities · 7 relationships
            </span>

          </div>

        </div>


        {/* Graph Details */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
              <Network size={18} />
            </div>

            <div>
              <h2 className="text-sm font-semibold text-white">
                Graph Intelligence
              </h2>

              <p className="text-xs text-slate-500">
                Selected entity
              </p>
            </div>

          </div>


          <div className="mt-6 rounded-lg border border-slate-800 bg-slate-950 p-4">

            <p className="text-xs uppercase tracking-wider text-slate-600">
              Central Entity
            </p>

            <p className="mt-2 text-lg font-semibold text-white">
              ShadowFox
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Threat Actor
            </p>

          </div>


          <div className="mt-5">

            <p className="text-xs font-medium uppercase tracking-wider text-slate-600">
              Connections
            </p>

            <div className="mt-3 space-y-2">

              <Connection
                icon={AtSign}
                label="@shadow_47"
                type="Handle"
              />

              <Connection
                icon={KeyRound}
                label="PGP Key"
                type="Cryptographic"
              />

              <Connection
                icon={Wallet}
                label="0x7A91...C42F"
                type="Wallet"
              />

              <Connection
                icon={Globe}
                label="Underground Forum"
                type="Platform"
              />

              <Connection
                icon={Globe}
                label="Marketplace"
                type="Platform"
              />

              <Connection
                icon={Globe}
                label="darkfox7x...onion"
                type="Onion Service"

              />

            </div>

          </div>


          <div className="mt-6 border-t border-slate-800 pt-5">

            <div className="flex items-center justify-between">

              <span className="text-xs text-slate-500">
                Relationship confidence
              </span>

              <span className="text-sm font-semibold text-emerald-400">
                94%
              </span>

            </div>

            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-800">

              <div
                className="h-full rounded-full bg-emerald-500"
                style={{ width: "94%" }}
              />

            </div>

          </div>

          <div className="mt-6">
            <button
              onClick={() => {
                window.history.pushState({}, "", "/timeline");
                window.dispatchEvent(new PopStateEvent("popstate"));
              }}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500"
            >
              View Investigation Timeline
            </button>
          </div>

        </div>

      </div>

    </div>
  );
}


/* Graph Node */

function GraphNode({
  icon: Icon,
  title,
  subtitle,
  position,
  active = false,
}: {
  icon: typeof User;
  title: string;
  subtitle: string;
  position: string;
  active?: boolean;
}) {
  return (
    <div
      className={`${position} z-10 w-44 rounded-xl border ${active
        ? "border-blue-500/50 bg-blue-500/10 shadow-lg shadow-blue-500/5"
        : "border-slate-700 bg-slate-900"
        } p-4`}
    >

      <div className="flex items-center gap-3">

        <div
          className={`flex h-9 w-9 items-center justify-center rounded-lg ${active
            ? "bg-blue-500/10 text-blue-400"
            : "bg-slate-800 text-slate-400"
            }`}
        >
          <Icon size={18} />
        </div>

        <div className="min-w-0">

          <p className="truncate text-sm font-medium text-white">
            {title}
          </p>

          <p className="mt-0.5 truncate text-[11px] text-slate-500">
            {subtitle}
          </p>

        </div>

      </div>

    </div>
  );
}


/* Connection */

function Connection({
  icon: Icon,
  label,
  type,
}: {
  icon: typeof User;
  label: string;
  type: string;
}) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-slate-800 bg-slate-950 p-3">

      <Icon size={16} className="text-slate-500" />

      <div className="min-w-0 flex-1">

        <p className="truncate text-xs font-medium text-slate-300">
          {label}
        </p>

        <p className="text-[10px] text-slate-600">
          {type}
        </p>

      </div>

    </div>
  );
}

export default RelationshipGraph;