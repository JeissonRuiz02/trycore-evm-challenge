import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ActivityForm } from "../components/ActivityForm";
import { ActivityTable } from "../components/ActivityTable";
import { MetricsCards } from "../components/MetricsCards";
import { PvEvAcChart } from "../components/PvEvAcChart";
import { api } from "../services/api";
import type { Activity, ActivityPayload, ProjectDetail as ProjectDetailType } from "../types";

export function ProjectDetail() {
  const { projectId } = useParams<{ projectId: string }>();
  const [project, setProject] = useState<ProjectDetailType | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!projectId) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const [detail, rows] = await Promise.all([
        api.getProject(projectId),
        api.listActivities(projectId),
      ]);
      setProject(detail);
      setActivities(rows);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar el proyecto");
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    void load();
  }, [load]);

  async function handleCreate(payload: ActivityPayload) {
    if (!projectId) {
      return;
    }
    await api.createActivity(projectId, payload);
    await load();
  }

  async function handleUpdate(id: string, payload: ActivityPayload) {
    await api.updateActivity(id, payload);
    await load();
  }

  async function handleDelete(id: string) {
    await api.deleteActivity(id);
    await load();
  }

  if (loading && !project) {
    return (
      <main className="page">
        <p className="muted">Cargando…</p>
      </main>
    );
  }

  if (!project) {
    return (
      <main className="page">
        <p className="error">{error ?? "Proyecto no encontrado"}</p>
        <Link to="/">Volver</Link>
      </main>
    );
  }

  return (
    <main className="page">
      <p>
        <Link to="/">← Proyectos</Link>
      </p>
      <header>
        <h1>{project.name}</h1>
        <p className="muted">{project.description || "Sin descripción"}</p>
      </header>

      {error ? <p className="error">{error}</p> : null}

      <h2>Consolidado</h2>
      <MetricsCards metrics={project.metrics} />

      <h2>PV vs EV vs AC</h2>
      <PvEvAcChart activities={activities} />

      <h2>Nueva actividad</h2>
      <div className="form-card">
        <ActivityForm submitLabel="Agregar actividad" onSubmit={handleCreate} />
      </div>

      <h2>Actividades</h2>
      <ActivityTable
        activities={activities}
        onUpdate={handleUpdate}
        onDelete={handleDelete}
      />
    </main>
  );
}
