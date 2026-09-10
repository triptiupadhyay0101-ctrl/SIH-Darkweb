import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  description: string;
  trend?: string;
  icon: LucideIcon;
  iconBg: string;
  iconColor: string;
  trendColor?: string;
}

function StatCard({
  title,
  value,
  description,
  trend,
  icon: Icon,
  iconBg,
  iconColor,
  trendColor = "text-emerald-400",
}: StatCardProps) {
  return (
    <div className="group rounded-xl border border-slate-800 bg-slate-900 p-5 transition duration-200 hover:-translate-y-0.5 hover:border-slate-700 hover:bg-slate-900/80">

      {/* Top section */}
      <div className="flex items-start justify-between">

        <div>
          <p className="text-sm font-medium text-slate-400">
            {title}
          </p>

          <h3 className="mt-3 text-3xl font-bold tracking-tight text-white">
            {value}
          </h3>
        </div>

        {/* Icon */}
        <div
          className={`flex h-10 w-10 items-center justify-center rounded-lg ${iconBg}`}
        >
          <Icon size={20} className={iconColor} />
        </div>

      </div>

      {/* Bottom section */}
      <div className="mt-4 flex items-center gap-2">

        {trend && (
          <span className={`text-xs font-semibold ${trendColor}`}>
            {trend}
          </span>
        )}

        <span className="text-xs text-slate-500">
          {description}
        </span>

      </div>

    </div>
  );
}

export default StatCard;