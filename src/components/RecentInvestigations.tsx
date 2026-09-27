import {
  ShieldAlert,
  ExternalLink,
} from "lucide-react";

const investigations = [
  {
    actor: "ShadowFox",
    identifier: "@shadow_47",
    threat: "Data Theft",
    confidence: 96,
    lastActivity: "12 min ago",
    status: "High",
  },
  {
    actor: "BlackCipher",
    identifier: "0x7A...91",
    threat: "Financial Fraud",
    confidence: 91,
    lastActivity: "34 min ago",
    status: "High",
  },
  {
    actor: "NightWolf",
    identifier: "@nightwolf",
    threat: "Credential Theft",
    confidence: 84,
    lastActivity: "1 hr ago",
    status: "Medium",
  },
  {
    actor: "GhostMarket",
    identifier: "ghostmarket.onion",
    threat: "Illegal Marketplace",
    confidence: 79,
    lastActivity: "2 hrs ago",
    status: "Medium",
  },
];

function RecentInvestigations() {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900">

      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 px-6 py-5">

        <div>
          <h2 className="text-lg font-semibold text-white">
            Recent Investigations
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Latest threat actor investigations
          </p>
        </div>

        <button className="flex items-center gap-2 text-sm font-medium text-blue-400 transition hover:text-blue-300">
          View all
          <ExternalLink size={15} />
        </button>

      </div>

      {/* Table */}
      <div className="overflow-x-auto">

        <table className="w-full">

          <thead>
            <tr className="border-b border-slate-800 text-left">

              <th className="px-6 py-4 text-xs font-medium uppercase tracking-wider text-slate-500">
                Actor
              </th>

              <th className="px-6 py-4 text-xs font-medium uppercase tracking-wider text-slate-500">
                Identifier
              </th>

              <th className="px-6 py-4 text-xs font-medium uppercase tracking-wider text-slate-500">
                Threat
              </th>

              <th className="px-6 py-4 text-xs font-medium uppercase tracking-wider text-slate-500">
                Confidence
              </th>

              <th className="px-6 py-4 text-xs font-medium uppercase tracking-wider text-slate-500">
                Last Activity
              </th>

              <th className="px-6 py-4 text-xs font-medium uppercase tracking-wider text-slate-500">
                Status
              </th>

            </tr>
          </thead>

          <tbody>

            {investigations.map((investigation) => (

              <tr
                key={investigation.actor}
                className="border-b border-slate-800/70 transition hover:bg-slate-800/40"
              >

                {/* Actor */}
                <td className="px-6 py-4">

                  <div className="flex items-center gap-3">

                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
                      <ShieldAlert size={18} />
                    </div>

                    <span className="font-medium text-white">
                      {investigation.actor}
                    </span>

                  </div>

                </td>

                {/* Identifier */}
                <td className="px-6 py-4 text-sm text-slate-400">
                  {investigation.identifier}
                </td>

                {/* Threat */}
                <td className="px-6 py-4">

                  <span className="rounded-md border border-slate-700 bg-slate-950 px-2.5 py-1 text-xs text-slate-300">
                    {investigation.threat}
                  </span>

                </td>

                {/* Confidence */}
                <td className="px-6 py-4">

                  <div className="flex items-center gap-3">

                    <div className="h-1.5 w-20 overflow-hidden rounded-full bg-slate-800">

                      <div
                        className="h-full rounded-full bg-blue-500"
                        style={{
                          width: `${investigation.confidence}%`,
                        }}
                      />

                    </div>

                    <span className="text-sm font-medium text-slate-300">
                      {investigation.confidence}%
                    </span>

                  </div>

                </td>

                {/* Last Activity */}
                <td className="px-6 py-4 text-sm text-slate-400">
                  {investigation.lastActivity}
                </td>

                {/* Status */}
                <td className="px-6 py-4">

                  <span
                    className={`rounded-full px-2.5 py-1 text-xs font-medium ${
                      investigation.status === "High"
                        ? "bg-red-500/10 text-red-400"
                        : "bg-yellow-500/10 text-yellow-400"
                    }`}
                  >
                    {investigation.status}
                  </span>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default RecentInvestigations;