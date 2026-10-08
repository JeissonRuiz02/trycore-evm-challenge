import type { Activity, ActivityPayload, Project, ProjectDetail } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  if (response.status === 204) {
    return undefined as T;
  }
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  listProjects: () => request<Project[]>("/projects"),
  getProject: (id: string) => request<ProjectDetail>(`/projects/${id}`),
  createProject: (payload: { name: string; description: string | null }) =>
    request<Project>("/projects", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  listActivities: (projectId: string) =>
    request<Activity[]>(`/projects/${projectId}/activities`),
  createActivity: (projectId: string, payload: ActivityPayload) =>
    request<Activity>(`/projects/${projectId}/activities`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updateActivity: (activityId: string, payload: ActivityPayload) =>
    request<Activity>(`/activities/${activityId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  deleteActivity: (activityId: string) =>
    request<void>(`/activities/${activityId}`, { method: "DELETE" }),
};
