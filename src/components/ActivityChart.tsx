import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

const activityData = [
  { day: "Mon", activity: 42 },
  { day: "Tue", activity: 65 },
  { day: "Wed", activity: 48 },
  { day: "Thu", activity: 78 },
  { day: "Fri", activity: 55 },
  { day: "Sat", activity: 88 },
  { day: "Sun", activity: 72 },
];

function ActivityChart() {
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={activityData}
          margin={{
            top: 10,
            right: 10,
            left: -20,
            bottom: 0,
          }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(148,163,184,0.1)"
          />

          <XAxis
            dataKey="day"
            tick={{
              fill: "#64748b",
              fontSize: 12,
            }}
            axisLine={false}
            tickLine={false}
          />

          <YAxis
            tick={{
              fill: "#64748b",
              fontSize: 12,
            }}
            axisLine={false}
            tickLine={false}
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a",
              border: "1px solid #1e293b",
              borderRadius: "8px",
              color: "#fff",
            }}
            labelStyle={{
              color: "#94a3b8",
            }}
          />

          <Area
            type="monotone"
            dataKey="activity"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.12}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ActivityChart;