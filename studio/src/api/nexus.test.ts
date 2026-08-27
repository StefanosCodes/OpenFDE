import { afterEach, describe, expect, it, vi } from "vitest";

import { getNexusHealth, listAccounts, NexusRequestError } from "./nexus";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Nexus client", () => {
  it("uses the same-origin development proxy", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ status: "ready", database: "ready" }), { status: 200 }),
    );

    await expect(getNexusHealth()).resolves.toEqual({ status: "ready", database: "ready" });
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/nexus/health",
      expect.objectContaining({ headers: { Accept: "application/json" } }),
    );
  });

  it("returns typed account pages", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ items: [], next_cursor: null }), { status: 200 }),
    );

    await expect(listAccounts()).resolves.toEqual({ items: [], next_cursor: null });
  });

  it("translates Nexus failures without leaking response bodies", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ detail: "Valid service authentication is required." }), {
        status: 401,
      }),
    );

    await expect(getNexusHealth()).rejects.toEqual(
      new NexusRequestError("Valid service authentication is required.", 401),
    );
  });
});
