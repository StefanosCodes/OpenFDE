import { expect, test } from "@playwright/test";

test("Studio routes and the Nexus contract are runnable together", async ({ page, request }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "OpenFDE.studio" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Agent projects" }).getByRole("link")).toHaveCount(
    8,
  );
  await expect(page.getByText(/Nexus ready/)).toBeVisible();
  await expect(page.getByText(/5 accounts reachable/)).toBeVisible();

  await page.getByRole("link", { name: /structured tool/i }).click();
  await expect(page).toHaveURL(/\/agents\/01-structured-tool$/);
  await expect(page.getByRole("heading", { name: "Structured Tool Agent" })).toBeVisible();
  await page.getByRole("link", { name: "Enter workspace" }).click();
  await expect(page.getByText("Agent runtime comes next.")).toBeVisible();

  const health = await request.get("http://127.0.0.1:8000/health");
  expect(health.ok()).toBeTruthy();
  expect(await health.json()).toEqual({ status: "ready", database: "ready" });
});
