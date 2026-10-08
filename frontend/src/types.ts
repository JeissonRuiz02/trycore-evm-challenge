export type MetricsStatus = {
  cost: string;
  schedule: string;
};

export type EVMMetrics = {
  pv: number;
  ev: number;
  cv: number;
  sv: number;
  cpi: number | null;
  spi: number | null;
  eac: number | null;
  vac: number | null;
  status: MetricsStatus;
};

export type Project = {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
};

export type ProjectDetail = Project & {
  metrics: EVMMetrics;
};

export type Activity = {
  id: string;
  project_id: string;
  name: string;
  bac: number;
  planned_progress: number;
  actual_progress: number;
  actual_cost: number;
  metrics: EVMMetrics;
};

export type ActivityPayload = {
  name: string;
  bac: number;
  planned_progress: number;
  actual_progress: number;
  actual_cost: number;
};
