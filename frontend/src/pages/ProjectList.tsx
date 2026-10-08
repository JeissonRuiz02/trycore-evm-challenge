import { useEffect, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { StatusBadge } from "../components/StatusBadge";
import { api } from "../services/api";
import type { ProjectDetail } from "../types";

export function ProjectList() {
  const [projects, setProjects] = useState<ProjectDetail[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const listed = await api.listProjects();
      const details = await Promise.all(
        listed.map((project) => api.getProject(project.id)),
      );
      setProjects(details);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudieron cargar los proyectos");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function handleCreate(event: FormEvent) {
    event.preventDefault();
    setError(null);
    try {
      await api.createProject({
        name: name.trim(),
        description: description.trim() || null,
      });
      setName("");
      setDescription("");
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo crear el proyecto");
    }
  }

  return (
    <main className="page">
      <header>
        <h1>Proyectos</h1>
        <p className="muted">
          Semáforo: verde si CPI y SPI van bien, rojo si el costo o el cronograma están mal.
        </p>
      </header>

      <form className="form-grid form-card" onSubmit={handleCreate}>
        <label>
          Nombre
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Descripción
          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>
        <div className="form-actions">
          <button type="submit">Crear proyecto</button>
        </div>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {loading ? <p className="muted">Cargando…</p> : null}

      <ul className="project-list">
        {projects.map((project) => {
          const costOk = project.metrics.status.cost === "Under Budget";
          const scheduleOk = project.metrics.status.schedule === "On Track/Ahead";
          const light = costOk && scheduleOk ? "ok" : "alert";
          return (
            <li key={project.id} className="project-item">
              <span className={`semaphore semaphore-${light}`} title="Estado global" />
              <div>
                <Link to={`/projects/${project.id}`}>{project.name}</Link>
                <p className="muted">{project.description || "Sin descripción"}</p>
              </div>
              <div className="project-badges">
                <StatusBadge kind="cost" label={project.metrics.status.cost} />
                <StatusBadge kind="schedule" label={project.metrics.status.schedule} />
              </div>
            </li>
          );
        })}
      </ul>
    </main>
  );
}
