import { useState } from "react";
import type { Activity, ActivityPayload } from "../types";
import { formatIndex, formatMoney } from "../utils/format";
import { ActivityForm } from "./ActivityForm";
import { StatusBadge } from "./StatusBadge";

type ActivityTableProps = {
  activities: Activity[];
  onUpdate: (id: string, payload: ActivityPayload) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
};

export function ActivityTable({
  activities,
  onUpdate,
  onDelete,
}: ActivityTableProps) {
  const [editingId, setEditingId] = useState<string | null>(null);

  if (activities.length === 0) {
    return <p className="muted">Todavía no hay actividades.</p>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Actividad</th>
            <th>BAC</th>
            <th>Plan %</th>
            <th>Real %</th>
            <th>AC</th>
            <th>PV</th>
            <th>EV</th>
            <th>CPI</th>
            <th>SPI</th>
            <th>Estado</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {activities.map((activity) =>
            editingId === activity.id ? (
              <tr key={activity.id}>
                <td colSpan={11}>
                  <ActivityForm
                    initial={activity}
                    submitLabel="Guardar cambios"
                    onCancel={() => setEditingId(null)}
                    onSubmit={async (payload) => {
                      await onUpdate(activity.id, payload);
                      setEditingId(null);
                    }}
                  />
                </td>
              </tr>
            ) : (
              <tr key={activity.id}>
                <td>{activity.name}</td>
                <td>{formatMoney(activity.bac)}</td>
                <td>{Math.round(activity.planned_progress * 100)}%</td>
                <td>{Math.round(activity.actual_progress * 100)}%</td>
                <td>{formatMoney(activity.actual_cost)}</td>
                <td>{formatMoney(activity.metrics.pv)}</td>
                <td>{formatMoney(activity.metrics.ev)}</td>
                <td>{formatIndex(activity.metrics.cpi)}</td>
                <td>{formatIndex(activity.metrics.spi)}</td>
                <td>
                  <StatusBadge kind="cost" label={activity.metrics.status.cost} />
                  <StatusBadge
                    kind="schedule"
                    label={activity.metrics.status.schedule}
                  />
                </td>
                <td className="row-actions">
                  <button type="button" className="secondary" onClick={() => setEditingId(activity.id)}>
                    Editar
                  </button>
                  <button
                    type="button"
                    className="danger"
                    onClick={() => onDelete(activity.id)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ),
          )}
        </tbody>
      </table>
    </div>
  );
}
