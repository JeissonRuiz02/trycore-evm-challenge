import type { EVMMetrics } from "../types";
import { formatIndex, formatMoney } from "../utils/format";
import { StatusBadge } from "./StatusBadge";

type MetricsCardsProps = {
  metrics: EVMMetrics;
};

const ITEMS: { key: keyof EVMMetrics; label: string }[] = [
  { key: "pv", label: "PV" },
  { key: "ev", label: "EV" },
  { key: "cv", label: "CV" },
  { key: "sv", label: "SV" },
  { key: "cpi", label: "CPI" },
  { key: "spi", label: "SPI" },
  { key: "eac", label: "EAC" },
  { key: "vac", label: "VAC" },
];

export function MetricsCards({ metrics }: MetricsCardsProps) {
  return (
    <section className="summary">
      <div className="summary-status">
        <StatusBadge kind="cost" label={metrics.status.cost} />
        <StatusBadge kind="schedule" label={metrics.status.schedule} />
      </div>
      <div className="cards">
        {ITEMS.map((item) => {
          const value = metrics[item.key];
          const display =
            item.key === "cpi" || item.key === "spi"
              ? formatIndex(value as number | null)
              : formatMoney(value as number | null);
          return (
            <article key={item.key} className="card">
              <p className="card-label">{item.label}</p>
              <p className="card-value">{display}</p>
            </article>
          );
        })}
      </div>
    </section>
  );
}
