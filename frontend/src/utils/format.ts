export function formatMoney(value: number | null): string {
  if (value === null || Number.isNaN(value)) {
    return "—";
  }
  return new Intl.NumberFormat("es-CO", {
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatIndex(value: number | null): string {
  if (value === null) {
    return "—";
  }
  return value.toFixed(2);
}

export function toPercentInput(ratio: number): string {
  return String(Math.round(ratio * 1000) / 10);
}

export function fromPercentInput(raw: string): number {
  return Number(raw) / 100;
}
