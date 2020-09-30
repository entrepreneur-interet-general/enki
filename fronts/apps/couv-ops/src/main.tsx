import { getStore } from "@fronts/core-couv-ops";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";

import App from "./app/app";
import { throwIfNotInArray, throwIfVariableUndefined } from "./app/envHelpers";

const httpClientKind = throwIfNotInArray(
  ["IN_MEMORY", "FLASK"],
  "NX_HTTP_CLIENT",
);

const backendUrl = throwIfVariableUndefined("NX_BACKEND_URL");

ReactDOM.render(
  <React.StrictMode>
    <Provider store={getStore(httpClientKind, backendUrl)}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById("root"),
);
