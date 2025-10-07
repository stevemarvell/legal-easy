// Simple TypeScript frontend that fetches a random number from the backend

const backendUrl = (window as any).BACKEND_URL || "http://localhost:8000";

function $(selector: string): HTMLElement {
  const el = document.querySelector(selector);
  if (!el) throw new Error(`Element not found: ${selector}`);
  return el as HTMLElement;
}

async function fetchRandom() {
  const btn = $("#btn") as HTMLButtonElement;
  const out = $("#output");
  btn.disabled = true;
  out.textContent = "Loading...";
  try {
    const res = await fetch(`${backendUrl}/random`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data: { value: number } = await res.json();
    out.textContent = String(data.value);
  } catch (err) {
    out.textContent = `Error: ${(err as Error).message}`;
  } finally {
    btn.disabled = false;
  }
}

function init() {
  const btn = $("#btn");
  btn.addEventListener("click", fetchRandom);
}

document.addEventListener("DOMContentLoaded", init);
