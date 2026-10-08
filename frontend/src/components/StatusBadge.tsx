type StatusBadgeProps = {
  kind: "cost" | "schedule";
  label: string;
};

export function StatusBadge({ kind, label }: StatusBadgeProps) {
  const ok =
    kind === "cost" ? label === "Under Budget" : label === "On Track/Ahead";
  return (
    <span className={`badge ${ok ? "badge-ok" : "badge-alert"}`}>{label}</span>
  );
}
