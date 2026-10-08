import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { Activity } from "../types";

type PvEvAcChartProps = {
  activities: Activity[];
};

export function PvEvAcChart({ activities }: PvEvAcChartProps) {
  if (activities.length === 0) {
    return <p className="muted">Agrega actividades para ver PV, EV y AC.</p>;
  }

  const data = activities.map((activity) => ({
    name: activity.name,
    PV: activity.metrics.pv,
    EV: activity.metrics.ev,
    AC: activity.actual_cost,
  }));

  return (
    <div className="chart">
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="PV" fill="#64748b" />
          <Bar dataKey="EV" fill="#2563eb" />
          <Bar dataKey="AC" fill="#dc2626" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
