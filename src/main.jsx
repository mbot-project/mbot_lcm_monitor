import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import LCMMonitorApp from "./app";

const root = createRoot(document.getElementById("app-root"));
root.render(
  <StrictMode>
    <LCMMonitorApp />
  </StrictMode>
);
