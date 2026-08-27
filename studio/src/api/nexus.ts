import type { components } from "./nexus.generated";

export type HealthResponse = components["schemas"]["HealthResponse"];
export type Account = components["schemas"]["AccountRead"];
export type AccountPage = components["schemas"]["Page_AccountRead_"];

const NEXUS_BASE_PATH = "/api/nexus";

export class NexusRequestError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "NexusRequestError";
  }
}

async function request<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${NEXUS_BASE_PATH}${path}`, {
    headers: { Accept: "application/json" },
    signal,
  });
  if (!response.ok) {
    let message = `Nexus request failed with status ${response.status}.`;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body.detail) {
        message = body.detail;
      }
    } catch {
      // Preserve the stable status-based fallback when the response is not JSON.
    }
    throw new NexusRequestError(message, response.status);
  }
  return (await response.json()) as T;
}

export function getNexusHealth(signal?: AbortSignal): Promise<HealthResponse> {
  return request<HealthResponse>("/health", signal);
}

export function listAccounts(signal?: AbortSignal): Promise<AccountPage> {
  return request<AccountPage>("/v1/accounts?limit=5", signal);
}
