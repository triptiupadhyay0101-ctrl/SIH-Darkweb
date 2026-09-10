import {
  Clock3,
  User,
  AtSign,
  KeyRound,
  Wallet,
  Globe,
  AlertTriangle,
  ArrowRight,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

const events = [
  {
    date: "14 Mar 2025",
    time: "09:42 UTC",
    title: "Persona First Observed",
    description:
      "The ShadowFox persona was first identified on an underground discussion platform.",
    type: "Identity",
    icon: User,
  },
  {
    date: "21 Mar 2025",
    time: "16:18 UTC",
    title: "New Handle Associated",
    description:
      "The username @shadow_47 was observed using a similar identity pattern.",
    type: "Handle",
    icon: AtSign,
  },
  {
    date: "03 Apr 2025",
    time: "11:27 UTC",
    title: "PGP Key Discovered",
    description:
      "A PGP fingerprint was linked to messages associated with the existing persona.",
    type: "Cryptographic",
    icon: KeyRound,
  },
  {
    date: "18 Apr 2025",
    time: "20:05 UTC",
    title: "Wallet Association",
    description:
      "A cryptocurrency wallet was identified in transactions connected with the investigated persona.",
    type: "Financial",
    icon: Wallet,
  },
  {
    date: "02 May 2025",
    time: "13:31 UTC",
    title: "Infrastructure Identified",
    description:
      "A previously observed onion service was associated with the actor's infrastructure.",
    type: "Infrastructure",
    icon: Globe,
  },
  {
    date: "17 May 2025",
    time: "22:14 UTC",
    title: "Activity Migration Detected",
    description:
      "The actor appeared to migrate activity from one platform to another.",
    type: "Migration",
    icon: ArrowRight,
  },
  {
    date: "01 Jun 2025",
    time: "08:56 UTC",
    title: "High-Confidence Match",
    description:
      "Behavioural and identity signals produced a high-confidence persona match.",
    type: "AI Analysis",
    icon: AlertTriangle,
  },
];

function Timeline() {
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
            Loading investigation timeline...
          </p>

          <p className="mt-1 text-xs text-slate-600">
            Preparing chronological activity
          </p>
        </div>
      </div>
    );
  }
  return (
    <div className="space-y-8">

      {/* Header */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">

        <div>
          <p className="text-sm font-medium uppercase tracking-wider text-blue-400">
            INVESTIGATION / ACTIVITY
          </p>

          <h1 className="mt-2 text-3xl font-semibold text-white">
            Investigation Timeline
          </h1>

          <p className="mt-2 max-w-2xl text-sm text-slate-400">
            Track identity changes, infrastructure activity, migrations and
            important investigation events over time.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-900 px-4 py-2.5">

          <Clock3 size={17} className="text-blue-400" />

          <span className="text-sm text-slate-300">
            7 Events
          </span>

        </div>

      </div>


      {/* Timeline Summary */}
      <div className="grid gap-5 md:grid-cols-3">

        <SummaryCard
          title="First Observed"
          value="14 Mar 2025"
          description="Initial persona detection"
        />

        <SummaryCard
          title="Latest Activity"
          value="01 Jun 2025"
          description="Most recent high-confidence event"
        />

        <SummaryCard
          title="Activity Span"
          value="79 Days"
          description="Observed investigation period"
        />

      </div>


      {/* Timeline */}
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

        <div className="mb-8">

          <h2 className="text-lg font-semibold text-white">
            Actor Activity
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Chronological view of significant observations
          </p>

        </div>


        <div className="relative">

          {/* Vertical Line */}
          <div className="absolute left-[19px] top-2 h-[calc(100%-16px)] w-px bg-slate-800" />


          <div className="space-y-8">

            {events.map((event, index) => {
              const Icon = event.icon;

              return (
                <div
                  key={`${event.date}-${event.title}`}
                  className="relative flex gap-5"
                >

                  {/* Timeline Icon */}
                  <div
                    className={`relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border ${index === events.length - 1
                      ? "border-blue-500/40 bg-blue-500/10 text-blue-400"
                      : "border-slate-700 bg-slate-950 text-slate-500"
                      }`}
                  >
                    <Icon size={17} />
                  </div>


                  {/* Event */}
                  <div className="min-w-0 flex-1 rounded-xl border border-slate-800 bg-slate-950 p-5 transition hover:border-slate-700">

                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">

                      <div>

                        <div className="flex flex-wrap items-center gap-2">

                          <h3 className="text-sm font-semibold text-white">
                            {event.title}
                          </h3>

                          <span className="rounded-md border border-slate-800 bg-slate-900 px-2 py-0.5 text-[10px] font-medium text-slate-500">
                            {event.type}
                          </span>

                        </div>

                        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
                          {event.description}
                        </p>

                      </div>


                      <div className="shrink-0 text-left sm:text-right">

                        <p className="text-xs font-medium text-slate-300">
                          {event.date}
                        </p>

                        <p className="mt-1 text-[11px] text-slate-600">
                          {event.time}
                        </p>

                      </div>

                    </div>

                  </div>

                </div>
              );
            })}

          </div>

        </div>

      </div>


      {/* Investigation Insight */}
      <div className="rounded-xl border border-blue-500/20 bg-blue-500/5 p-5">

        <div className="flex items-start gap-4">

          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
            <Clock3 size={19} />
          </div>

          <div>

            <h3 className="text-sm font-semibold text-white">
              Investigation Insight
            </h3>

            <p className="mt-1 text-sm leading-6 text-slate-400">
              The timeline indicates progressive identity and infrastructure
              linkage. Multiple independent signals were observed before the
              system generated a high-confidence attribution result.
            </p>

          </div>

        </div>

      </div>

      <div className="flex justify-end">
        <button
          onClick={() => navigate("/ai-results")}
          className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500"
        >
          Continue to AI Analysis
        </button>
      </div>

    </div>
  );
}


/* Summary Card */

function SummaryCard({
  title,
  value,
  description,
}: {
  title: string;
  value: string;
  description: string;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">

      <p className="text-xs font-medium uppercase tracking-wider text-slate-600">
        {title}
      </p>

      <p className="mt-3 text-xl font-semibold text-white">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {description}
      </p>


    </div>
  );
}

export default Timeline;