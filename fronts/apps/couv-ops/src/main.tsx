import { getStore } from "@fronts/core-couv-ops";
import { throwIfNotInArray, throwIfVariableUndefined } from "@fronts/utilities";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { App } from "./app/app";

const processEnv = process.env;

const httpClientKind = throwIfNotInArray({
  processEnv,
  authorizedValues: ["IN_MEMORY", "FLASK"],
  variableName: "NX_HTTP_CLIENT",
});

const backendUrl = throwIfVariableUndefined({
  processEnv,
  variableName: "NX_BACKEND_URL",
});

ReactDOM.render(
  <React.StrictMode>
    <Provider store={getStore(httpClientKind, backendUrl)}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById("root"),
);
