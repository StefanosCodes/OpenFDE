import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { AppRoutes } from "./app";
import { agents } from "./lib/agents";

function renderRoute(route: string) {
  return render(
    <MemoryRouter initialEntries={[route]}>
      <AppRoutes />
    </MemoryRouter>,
  );
}

function mockNexusReady() {
  vi.spyOn(globalThis, "fetch")
    .mockResolvedValueOnce(
      new Response(JSON.stringify({ status: "ready", database: "ready" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    )
    .mockResolvedValueOnce(
      new Response(JSON.stringify({ items: [{ id: "one" }], next_cursor: null }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
}

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("OpenFDE Studio routes", () => {
  it("renders the eight-project curriculum and Nexus readiness", async () => {
    mockNexusReady();
    renderRoute("/");

    expect(screen.getByRole("heading", { name: "OpenFDE.studio" })).toBeInTheDocument();
    expect(screen.getAllByRole("link")).toHaveLength(10);
    for (const agent of agents) {
      expect(screen.getByRole("link", { name: new RegExp(agent.shortName) })).toBeInTheDocument();
    }
    expect(await screen.findByText(/Nexus ready/)).toBeInTheDocument();
    expect(screen.getByText(/1 accounts reachable/)).toBeInTheDocument();
  });

  it("renders every agent overview from its catalog route", () => {
    for (const agent of agents) {
      const view = renderRoute(`/agents/${agent.slug}`);
      expect(screen.getByRole("heading", { name: agent.name })).toBeInTheDocument();
      expect(screen.getByText(agent.deliverable)).toBeInTheDocument();
      view.unmount();
    }
  });

  it("keeps Agent 1 workspace honest about the runtime boundary", () => {
    renderRoute("/agents/01-structured-tool/workspace");

    expect(screen.getByRole("heading", { name: "Structured Tool Agent" })).toBeInTheDocument();
    expect(screen.getByText("Agent runtime comes next.")).toBeInTheDocument();
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  });

  it("navigates to a catalog-driven overview", async () => {
    mockNexusReady();
    const user = userEvent.setup();
    renderRoute("/");

    await user.click(screen.getByRole("link", { name: /structured tool/i }));

    expect(screen.getByRole("heading", { name: "Structured Tool Agent" })).toBeInTheDocument();
    await waitFor(() => expect(document.title).toContain("Structured Tool Agent"));
  });

  it("renders a not-found boundary for unknown projects", () => {
    renderRoute("/agents/not-real");

    expect(screen.getByText("this route is not an agent project.")).toBeInTheDocument();
  });
});
