type StatusBadgeProps = {
  kind: "cost" | "schedule";
  label: string;
};

const COST_LABELS: Record<string, string> = {
  "Under Budget": "Bajo presupuesto",
  "Over Budget": "Sobre presupuesto",
};

const SCHEDULE_LABELS: Record<string, string> = {
  "On Track/Ahead": "En tiempo / adelantado",
  "Behind Schedule": "Atrasado",
};

export function StatusBadge({ kind, label }: StatusBadgeProps) {
  const ok =
    kind === "cost" ? label === "Under Budget" : label === "On Track/Ahead";
  const text =
    kind === "cost"
      ? (COST_LABELS[label] ?? label)
      : (SCHEDULE_LABELS[label] ?? label);
  return (
    <span className={`badge ${ok ? "badge-ok" : "badge-alert"}`}>{text}</span>
  );
}
