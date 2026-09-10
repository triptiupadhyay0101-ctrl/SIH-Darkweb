import {
  User,
  ShieldAlert,
  KeyRound,
  Wallet,
  Globe,
  AtSign,
  ExternalLink,
  Activity,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function ActorProfile() {

  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);

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
            Loading actor intelligence...
          </p>

          <p className="mt-1 text-xs text-slate-600">
            Retrieving investigation profile
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">

      {/* Page Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">

        <div>
          <p className="text-sm font-medium uppercase tracking-wider text-blue-400">
            INVESTIGATION / ACTOR
          </p>

          <h1 className="mt-2 text-3xl font-semibold text-white">
            ShadowFox
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            Threat actor profile and attribution intelligence
          </p>
        </div>

        <div className="flex items-center gap-3">

          <span className="rounded-full border border-red-500/20 bg-red-500/10 px-3 py-1.5 text-xs font-medium text-red-400">
            High Risk
          </span>

          <button
            onClick={() => navigate("/relationship-graph")}
            className="flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-900 px-4 py-2 text-sm text-slate-300 transition hover:border-slate-700 hover:text-white"
          >
            <ExternalLink size={16} />
            View Relationship Graph
          </button>

        </div>

      </div>


      {/* Profile Overview */}
      <div className="grid gap-5 lg:grid-cols-3">

        {/* Identity Card */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 lg:col-span-2">

          <div className="flex items-start gap-5">

            <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
              <User size={30} />
            </div>

            <div className="min-w-0">

              <h2 className="text-xl font-semibold text-white">
                ShadowFox
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Primary threat actor identifier
              </p>

              <div className="mt-4 flex flex-wrap gap-2">

                <span className="rounded-md border border-slate-700 bg-slate-950 px-2.5 py-1 text-xs text-slate-400">
                  Financial Fraud
                </span>

                <span className="rounded-md border border-slate-700 bg-slate-950 px-2.5 py-1 text-xs text-slate-400">
                  Data Theft
                </span>

                <span className="rounded-md border border-slate-700 bg-slate-950 px-2.5 py-1 text-xs text-slate-400">
                  Dark Web
                </span>

              </div>

            </div>

          </div>


          {/* Description */}
          <div className="mt-7 border-t border-slate-800 pt-6">

            <h3 className="text-sm font-medium text-white">
              Actor Summary
            </h3>

            <p className="mt-2 text-sm leading-6 text-slate-400">
              ShadowFox is an identified online persona associated with
              multiple suspicious activities across underground platforms.
              The profile aggregates identity signals, infrastructure,
              cryptocurrency indicators and behavioural evidence.
            </p>

          </div>

        </div>


        {/* Confidence */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400">
              <ShieldAlert size={20} />
            </div>

            <div>
              <p className="text-sm font-medium text-white">
                Attribution Confidence
              </p>

              <p className="text-xs text-slate-500">
                AI-assisted assessment
              </p>
            </div>

          </div>


          <div className="mt-8 flex items-end gap-2">

            <span className="text-5xl font-bold text-white">
              96
            </span>

            <span className="mb-1 text-xl text-slate-500">
              %
            </span>

          </div>


          <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">

            <div
              className="h-full rounded-full bg-emerald-500"
              style={{ width: "96%" }}
            />

          </div>


          <div className="mt-4 flex items-center justify-between text-xs">

            <span className="text-slate-500">
              Confidence level
            </span>

            <span className="font-medium text-emerald-400">
              Very High
            </span>

          </div>

        </div>

      </div>


      {/* Identity Indicators */}
      <div>

        <div className="mb-4">

          <h2 className="text-lg font-semibold text-white">
            Identity Indicators
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Known identifiers and associated infrastructure
          </p>

        </div>


        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">

          <IndicatorCard
            icon={AtSign}
            title="Known Handles"
            value="7"
            detail="@shadow_47"
          />

          <IndicatorCard
            icon={KeyRound}
            title="PGP Keys"
            value="2"
            detail="Fingerprint linked"
          />

          <IndicatorCard
            icon={Wallet}
            title="Wallets"
            value="4"
            detail="Crypto addresses"
          />

          <IndicatorCard
            icon={Globe}
            title="Platforms"
            value="9"
            detail="Related platforms"
          />

        </div>

      </div>


      {/* Known Aliases & Handles */}
      <div className="grid gap-5 lg:grid-cols-2">

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center justify-between">

            <div>
              <h2 className="text-lg font-semibold text-white">
                Known Aliases
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Previously observed identities
              </p>
            </div>

            <User size={19} className="text-slate-600" />

          </div>


          <div className="mt-6 space-y-3">

            <Alias name="ShadowFox" confidence="96%" />
            <Alias name="FoxShadow" confidence="89%" />
            <Alias name="SFX47" confidence="74%" />
            <Alias name="NightFox" confidence="68%" />

          </div>

        </div>


        {/* Handles */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center justify-between">

            <div>
              <h2 className="text-lg font-semibold text-white">
                Known Handles
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Usernames observed across platforms
              </p>
            </div>

            <AtSign size={19} className="text-slate-600" />

          </div>


          <div className="mt-6 space-y-3">

            <Handle
              handle="@shadow_47"
              platform="Underground Forum"
            />

            <Handle
              handle="shadowfox"
              platform="Encrypted Chat"
            />

            <Handle
              handle="SFX47"
              platform="Marketplace"
            />

            <Handle
              handle="fox_shadow"
              platform="Discussion Board"
            />

          </div>

        </div>

      </div>


      {/* Technical Indicators */}
      <div className="rounded-xl border border-slate-800 bg-slate-900">

        <div className="border-b border-slate-800 px-6 py-5">

          <h2 className="text-lg font-semibold text-white">
            Technical Indicators
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Cryptographic and infrastructure identifiers
          </p>

        </div>


        <div className="divide-y divide-slate-800">

          <TechnicalRow
            icon={KeyRound}
            title="PGP Fingerprint"
            value="8A42 7F91 3C62 91AB 4F28"
          />

          <TechnicalRow
            icon={Wallet}
            title="Primary Wallet"
            value="0x7A91...C42F"
          />

          <TechnicalRow
            icon={Globe}
            title="Known Onion Service"
            value="shadowfox47.onion"
          />

          <TechnicalRow
            icon={Activity}
            title="First Observed"
            value="14 March 2025"
          />

        </div>

      </div>
      {/* Investigation Actions */}
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

        <div>
          <h2 className="text-lg font-semibold text-white">
            Continue Investigation
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Explore this actor's relationships, activity timeline and
            AI-assisted analysis.
          </p>
        </div>

        <div className="mt-5 flex flex-wrap gap-3">

          <button
            onClick={() => navigate("/relationship-graph")}
            className="rounded-lg border border-slate-800 bg-slate-950 px-4 py-2.5 text-sm text-slate-300 transition hover:border-slate-700 hover:text-white"
          >
            Relationship Graph
          </button>

          <button
            onClick={() => navigate("/timeline")}
            className="rounded-lg border border-slate-800 bg-slate-950 px-4 py-2.5 text-sm text-slate-300 transition hover:border-slate-700 hover:text-white"
          >
            View Timeline
          </button>

          <button
            onClick={() => navigate("/ai-results")}
            className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500"
          >
            View AI Analysis
          </button>

        </div>

      </div>
    </div>
  );
}


/* Indicator Card */

function IndicatorCard({
  icon: Icon,
  title,
  value,
  detail,
}: {
  icon: typeof User;
  title: string;
  value: string;
  detail: string;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5 transition hover:border-slate-700">

      <div className="flex items-center justify-between">

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-800 text-slate-400">
          <Icon size={18} />
        </div>

        <span className="text-2xl font-bold text-white">
          {value}
        </span>

      </div>

      <p className="mt-4 text-sm font-medium text-slate-300">
        {title}
      </p>

      <p className="mt-1 truncate text-xs text-slate-500">
        {detail}
      </p>

    </div>
  );
}


/* Alias */

function Alias({
  name,
  confidence,
}: {
  name: string;
  confidence: string;
}) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950 px-4 py-3">

      <span className="text-sm text-slate-300">
        {name}
      </span>

      <span className="text-xs font-medium text-emerald-400">
        {confidence}
      </span>

    </div>
  );
}


/* Handle */

function Handle({
  handle,
  platform,
}: {
  handle: string;
  platform: string;
}) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950 px-4 py-3">

      <span className="text-sm font-medium text-slate-300">
        {handle}
      </span>

      <span className="text-xs text-slate-500">
        {platform}
      </span>

    </div>
  );
}


/* Technical Row */

function TechnicalRow({
  icon: Icon,
  title,
  value,
}: {
  icon: typeof User;
  title: string;
  value: string;
}) {
  return (
    <div className="flex flex-col gap-2 px-6 py-4 sm:flex-row sm:items-center">

      <div className="flex items-center gap-3 sm:w-56">

        <Icon size={17} className="text-slate-500" />

        <span className="text-sm text-slate-400">
          {title}
        </span>

      </div>

      <span className="font-mono text-sm text-slate-300">
        {value}
      </span>


    </div>
  );
}

export default ActorProfile;