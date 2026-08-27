import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import { AppRoutes } from "./app";
import "./styles.css";

const root = document.getElementById("root");

if (!root) {
  throw new Error("OpenFDE Studio root element is missing.");
}

createRoot(root).render(
  <StrictMode>
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  </StrictMode>,
);
