import {
  Users,
  ShieldAlert,
  BrainCircuit,
  Activity,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import StatCard from "../components/StatCard";
import ActivityChart from "../components/ActivityChart";
import RecentInvestigations from "../components/RecentInvestigations";

function Dashboard() {
  const navigate = useNavigate();
  return (
    <div className="space-y-8">

      {/* Page Header */}
      <div>
        <p className="text-sm font-medium text-blue-400">
          OVERVIEW
        </p>

        <h1 className="mt-1 text-3xl font-bold tracking-tight text-white">
          Threat Intelligence Dashboard
        </h1>

        <p className="mt-2 max-w-2xl text-sm text-slate-400">
          Monitor threat actors, investigate relationships and review
          AI-powered attribution results.
        </p>
      </div>


      {/* KPI Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">

        <StatCard
          title="Total Actors"
          value="1,284"
          description="vs. last month"
          trend="+12.5%"
          icon={Users}
          iconBg="bg-blue-500/10"
          iconColor="text-blue-400"
        />

        <StatCard
          title="Threat Categories"
          value="18"
          description="active categories"
          trend="+4.2%"
          icon={ShieldAlert}
          iconBg="bg-red-500/10"
          iconColor="text-red-400"
          trendColor="text-red-400"
        />

        <StatCard
          title="AI Matches"
          value="342"
          description="high confidence"
          trend="+8.1%"
          icon={BrainCircuit}
          iconBg="bg-purple-500/10"
          iconColor="text-purple-400"
          trendColor="text-purple-400"
        />

        <StatCard
          title="Recent Activity"
          value="76"
          description="last 24 hours"
          trend="+16.4%"
          icon={Activity}
          iconBg="bg-emerald-500/10"
          iconColor="text-emerald-400"
        />

      </div>


      {/* Dashboard Content */}
      <div className="grid grid-cols-1 gap-5 xl:grid-cols-3">

        {/* Activity Overview */}
        <div className="xl:col-span-2 rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center justify-between">

            <div>
              <h2 className="text-lg font-semibold text-white">
                Activity Overview
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Threat actor activity over the last 7 days
              </p>
            </div>

            <span className="rounded-md border border-slate-800 bg-slate-950 px-3 py-1.5 text-xs text-slate-400">
              Last 7 days
            </span>

          </div>

          <div className="mt-6">
            <ActivityChart />
          </div>

        </div>

        {/* Recent Investigations */}
        <div className="mt-8">
          <RecentInvestigations />
        </div>


        {/* Threat Categories */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div>
            <h2 className="text-lg font-semibold text-white">
              Threat Categories
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Distribution of identified threats
            </p>
          </div>

          <div className="mt-7 space-y-5">

            <ThreatCategory
              name="Data Theft"
              percentage={42}
              color="bg-red-500"
            />

            <ThreatCategory
              name="Fraud"
              percentage={28}
              color="bg-orange-500"
            />

            <ThreatCategory
              name="Hacking Services"
              percentage={18}
              color="bg-purple-500"
            />

            <ThreatCategory
              name="Other"
              percentage={12}
              color="bg-blue-500"
            />

          </div>

        </div>

      </div>


      {/* Recent Investigations */}
      <div className="rounded-xl border border-slate-800 bg-slate-900">

        <div className="flex items-center justify-between border-b border-slate-800 px-6 py-5">

          <div>
            <h2 className="text-lg font-semibold text-white">
              Recent Investigations
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Latest threat actor investigations
            </p>
          </div>

          <button
            onClick={() => navigate("/actor-profile")}
            className="text-sm font-medium text-blue-400 hover:text-blue-300"
          >
            View all
          </button>

        </div>


        <div className="divide-y divide-slate-800">

          <Investigation
            actor="ShadowFox"
            identifier="shadowfox7x3.onion"
            type="Onion Address"
            risk="High"
            confidence="96%"
          />

          <Investigation
            actor="DarkSpecter"
            identifier="0x83F...91A2"
            type="Wallet"
            risk="Medium"
            confidence="82%"
          />

          <Investigation
            actor="PhantomX"
            identifier="A9F3...7B21"
            type="PGP Key"
            risk="Low"
            confidence="61%"
          />

        </div>

      </div>

    </div>
  );
}


/* Threat Category Component */

function ThreatCategory({
  name,
  percentage,
  color,
}: {
  name: string;
  percentage: number;
  color: string;
}) {
  return (
    <div>

      <div className="mb-2 flex items-center justify-between">

        <span className="text-sm text-slate-300">
          {name}
        </span>

        <span className="text-xs font-medium text-slate-500">
          {percentage}%
        </span>

      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-800">

        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${percentage}%` }}
        />

      </div>

    </div>
  );
}


/* Investigation Component */

function Investigation({
  actor,
  identifier,
  type,
  risk,
  confidence,
}: {
  actor: string;
  identifier: string;
  type: string;
  risk: string;
  confidence: string;
}) {
  const navigate = useNavigate();

  const riskStyles = {
    High: "bg-red-500/10 text-red-400 border-red-500/20",
    Medium: "bg-orange-500/10 text-orange-400 border-orange-500/20",
    Low: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  };

  return (
    <div
      onClick={() => navigate("/actor-profile")}
      className="flex cursor-pointer flex-col gap-4 px-6 py-4 transition hover:bg-slate-900 sm:flex-row sm:items-center sm:justify-between"
    >
      <div className="flex items-center gap-4">

        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-800 text-sm font-semibold text-slate-300">
          {actor.charAt(0)}
        </div>

        <div>
          <p className="text-sm font-medium text-white">
            {actor}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            {type} · {identifier}
          </p>
        </div>

      </div>


      <div className="flex items-center gap-6">

        <span
          className={`rounded-full border px-3 py-1 text-xs font-medium ${riskStyles[risk as keyof typeof riskStyles]
            }`}
        >
          {risk} Risk
        </span>

        <div className="text-right">

          <p className="text-xs text-slate-500">
            Confidence
          </p>

          <p className="mt-1 text-sm font-semibold text-white">
            {confidence}
          </p>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;