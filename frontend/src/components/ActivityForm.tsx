import { useState, type FormEvent } from "react";
import type { Activity, ActivityPayload } from "../types";
import { fromPercentInput, toPercentInput } from "../utils/format";

type ActivityFormProps = {
  initial?: Activity;
  submitLabel: string;
  onSubmit: (payload: ActivityPayload) => Promise<void>;
  onCancel?: () => void;
};

export function ActivityForm({
  initial,
  submitLabel,
  onSubmit,
  onCancel,
}: ActivityFormProps) {
  const [name, setName] = useState(initial?.name ?? "");
  const [bac, setBac] = useState(initial ? String(initial.bac) : "");
  const [planned, setPlanned] = useState(
    initial ? toPercentInput(initial.planned_progress) : "",
  );
  const [actual, setActual] = useState(
    initial ? toPercentInput(initial.actual_progress) : "",
  );
  const [cost, setCost] = useState(initial ? String(initial.actual_cost) : "");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setSaving(true);
    try {
      await onSubmit({
        name: name.trim(),
        bac: Number(bac),
        planned_progress: fromPercentInput(planned),
        actual_progress: fromPercentInput(actual),
        actual_cost: Number(cost),
      });
      if (!initial) {
        setName("");
        setBac("");
        setPlanned("");
        setActual("");
        setCost("");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="form-grid" onSubmit={handleSubmit}>
      <label>
        Nombre
        <input value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <label>
        BAC
        <input
          type="number"
          min="0.01"
          step="0.01"
          value={bac}
          onChange={(e) => setBac(e.target.value)}
          required
        />
      </label>
      <label>
        Planificado %
        <input
          type="number"
          min="0"
          max="100"
          step="0.1"
          value={planned}
          onChange={(e) => setPlanned(e.target.value)}
          required
        />
      </label>
      <label>
        Real %
        <input
          type="number"
          min="0"
          max="100"
          step="0.1"
          value={actual}
          onChange={(e) => setActual(e.target.value)}
          required
        />
      </label>
      <label>
        Costo real (AC)
        <input
          type="number"
          min="0"
          step="0.01"
          value={cost}
          onChange={(e) => setCost(e.target.value)}
          required
        />
      </label>
      {error ? <p className="error">{error}</p> : null}
      <div className="form-actions">
        <button type="submit" disabled={saving}>
          {saving ? "Guardando…" : submitLabel}
        </button>
        {onCancel ? (
          <button type="button" className="secondary" onClick={onCancel}>
            Cancelar
          </button>
        ) : null}
      </div>
    </form>
  );
}
