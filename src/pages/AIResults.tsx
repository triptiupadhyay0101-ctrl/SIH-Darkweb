import {
  Brain,
  ShieldCheck,
  User,
  MessageSquare,
  Clock3,
  Globe,
  Wallet,
  KeyRound,
  CheckCircle2,
  AlertTriangle,
  FileText,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

function AIResults() {
  const navigate = useNavigate();
  return (
    <div className="space-y-8">

      {/* Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">

        <div>
          <p className="text-sm font-medium uppercase tracking-wider text-blue-400">
            INVESTIGATION / AI ANALYSIS
          </p>

          <h1 className="mt-2 text-3xl font-semibold text-white">
            AI Attribution Results
          </h1>

          <p className="mt-2 max-w-2xl text-sm text-slate-400">
            AI-assisted analysis of persona similarity, behavioural patterns
            and attribution evidence.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-lg border border-emerald-500/20 bg-emerald-500/5 px-4 py-2.5">

          <ShieldCheck size={17} className="text-emerald-400" />

          <span className="text-sm font-medium text-emerald-400">
            Analysis Complete
          </span>

        </div>

      </div>


      {/* Main Score */}
      <div className="grid gap-5 lg:grid-cols-3">

        {/* Attribution Score */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6 lg:col-span-2">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
              <Brain size={21} />
            </div>

            <div>
              <h2 className="text-sm font-semibold text-white">
                Attribution Confidence
              </h2>

              <p className="text-xs text-slate-500">
                Overall AI assessment
              </p>
            </div>

          </div>


          <div className="mt-8 flex flex-col items-center justify-center">

            <div className="relative flex h-48 w-48 items-center justify-center rounded-full border-[12px] border-slate-800">

              <div className="absolute inset-[-12px] rounded-full border-[12px] border-emerald-500 border-b-transparent border-l-transparent rotate-[-25deg]" />

              <div className="text-center">

                <p className="text-6xl font-bold text-white">
                  96%
                </p>

                <p className="mt-1 text-sm font-medium text-emerald-400">
                  Very High
                </p>

              </div>

            </div>

            <p className="mt-6 max-w-lg text-center text-sm leading-6 text-slate-400">
              The system found strong evidence connecting the investigated
              personas and identifiers to the same underlying threat actor.
            </p>

          </div>

        </div>


        {/* Subject */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

          <p className="text-xs font-medium uppercase tracking-wider text-slate-600">
            Investigated Persona
          </p>

          <div className="mt-5 flex items-center gap-4">

            <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
              <User size={26} />
            </div>

            <div>
              <h2 className="text-xl font-semibold text-white">
                ShadowFox
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Threat actor
              </p>
            </div>

          </div>


          <div className="mt-7 space-y-4">

            <MiniStat
              label="Persona Matches"
              value="7"
            />

            <MiniStat
              label="Evidence Signals"
              value="18"
            />

            <MiniStat
              label="Related Platforms"
              value="9"
            />

          </div>

        </div>

      </div>


      {/* Confidence Breakdown */}
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

        <div>
          <h2 className="text-lg font-semibold text-white">
            Confidence Breakdown
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Individual signals contributing to the attribution score
          </p>
        </div>


        <div className="mt-7 grid gap-5 md:grid-cols-2">

          <ConfidenceBar
            icon={User}
            title="Persona Similarity"
            description="Identity and alias similarity"
            value={97}
          />

          <ConfidenceBar
            icon={MessageSquare}
            title="Writing Style"
            description="Stylometric similarity across posts"
            value={94}
          />

          <ConfidenceBar
            icon={Clock3}
            title="Behavioural Pattern"
            description="Activity timing and behavioural signals"
            value={91}
          />

          <ConfidenceBar
            icon={Globe}
            title="Infrastructure Link"
            description="Related domains and onion services"
            value={96}
          />

        </div>

      </div>


      {/* Evidence */}
      <div className="grid gap-5 lg:grid-cols-2">

        {/* Supporting Evidence */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400">
              <CheckCircle2 size={18} />
            </div>

            <div>
              <h2 className="text-lg font-semibold text-white">
                Supporting Evidence
              </h2>

              <p className="text-xs text-slate-500">
                Signals strengthening the attribution
              </p>
            </div>

          </div>


          <div className="mt-6 space-y-3">

            <Evidence
              icon={User}
              title="Alias similarity"
              description="Multiple aliases share strong identity characteristics."
            />

            <Evidence
              icon={MessageSquare}
              title="Stylometric match"
              description="Writing patterns show a high degree of similarity."
            />

            <Evidence
              icon={Wallet}
              title="Wallet association"
              description="A cryptocurrency address is linked to the investigated persona."
            />

            <Evidence
              icon={KeyRound}
              title="PGP correlation"
              description="Cryptographic identity signals overlap with known activity."
            />

          </div>

        </div>


        {/* Behaviour Analysis */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-purple-500/10 text-purple-400">
              <Brain size={18} />
            </div>

            <div>
              <h2 className="text-lg font-semibold text-white">
                Behaviour Analysis
              </h2>

              <p className="text-xs text-slate-500">
                Observed behavioural characteristics
              </p>
            </div>

          </div>


          <div className="mt-6 space-y-5">

            <Behaviour
              title="Activity Pattern"
              value="Consistent"
              description="Similar activity windows observed across platforms."
            />

            <Behaviour
              title="Communication Style"
              value="Highly Similar"
              description="Vocabulary and sentence structure show strong overlap."
            />

            <Behaviour
              title="Platform Migration"
              value="Detected"
              description="Activity moved between related underground platforms."
            />

          </div>

        </div>

      </div>


      {/* AI Explanation */}
      <div className="rounded-xl border border-blue-500/20 bg-blue-500/5 p-6">

        <div className="flex items-start gap-4">

          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
            <FileText size={19} />
          </div>

          <div>

            <h2 className="text-sm font-semibold text-white">
              AI Attribution Explanation
            </h2>

            <p className="mt-2 text-sm leading-7 text-slate-400">
              The attribution model identified multiple independent signals
              connecting ShadowFox with the observed handles, cryptographic
              identifiers, wallet activity and infrastructure. Persona
              similarity and behavioural characteristics provided the strongest
              supporting evidence. The combined signals resulted in a 96%
              attribution confidence score.
            </p>

          </div>

        </div>

      </div>


      {/* Warning */}
      <div className="flex items-start gap-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-5">

        <AlertTriangle
          size={19}
          className="mt-0.5 shrink-0 text-amber-400"
        />

        <div>

          <h3 className="text-sm font-semibold text-amber-300">
            Analyst Review Recommended
          </h3>

          <p className="mt-1 text-sm leading-6 text-slate-500">
            AI attribution results are investigative indicators and should be
            reviewed alongside source evidence before making an operational
            decision.
          </p>

        </div>

      </div>

      <div className="flex justify-end">
        <button
          onClick={() => navigate("/export")}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500"
        >
          <FileText size={17} />
          Export Investigation Report
        </button>
      </div>

    </div>
  );
}


/* Mini Stat */

function MiniStat({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between border-b border-slate-800 pb-3">

      <span className="text-sm text-slate-500">
        {label}
      </span>

      <span className="text-sm font-semibold text-white">
        {value}
      </span>

    </div>
  );
}


/* Confidence Bar */

function ConfidenceBar({
  icon: Icon,
  title,
  description,
  value,
}: {
  icon: typeof User;
  title: string;
  description: string;
  value: number;
}) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-950 p-4">

      <div className="flex items-center gap-3">

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900 text-slate-400">
          <Icon size={17} />
        </div>

        <div className="min-w-0 flex-1">

          <div className="flex items-center justify-between gap-3">

            <p className="text-sm font-medium text-slate-300">
              {title}
            </p>

            <span className="text-sm font-semibold text-emerald-400">
              {value}%
            </span>

          </div>

          <p className="mt-1 text-xs text-slate-600">
            {description}
          </p>

        </div>

      </div>


      <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-800">

        <div
          className="h-full rounded-full bg-emerald-500"
          style={{ width: `${value}%` }}
        />

      </div>

    </div>
  );
}


/* Evidence */

function Evidence({
  icon: Icon,
  title,
  description,
}: {
  icon: typeof User;
  title: string;
  description: string;
}) {
  return (
    <div className="flex gap-3 rounded-lg border border-slate-800 bg-slate-950 p-3">

      <Icon
        size={16}
        className="mt-0.5 shrink-0 text-emerald-400"
      />

      <div>

        <p className="text-sm font-medium text-slate-300">
          {title}
        </p>

        <p className="mt-1 text-xs leading-5 text-slate-600">
          {description}
        </p>

      </div>

    </div>
  );
}


/* Behaviour */

function Behaviour({
  title,
  value,
  description,
}: {
  title: string;
  value: string;
  description: string;
}) {
  return (
    <div>

      <div className="flex items-center justify-between">

        <p className="text-sm font-medium text-slate-300">
          {title}
        </p>

        <span className="rounded-md bg-purple-500/10 px-2 py-1 text-[10px] font-medium text-purple-400">
          {value}
        </span>

      </div>

      <p className="mt-2 text-xs leading-5 text-slate-600">
        {description}
      </p>

    </div>
  );
}

export default AIResults;