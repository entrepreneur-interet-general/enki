import { getStore } from "@fronts/core-couv-ops";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";

import App from "./app/app";
import { throwIfNotInArray } from "./app/envHelpers";

const httpClientKind = throwIfNotInArray(
  ["IN_MEMORY", "FLASK"],
  "NX_HTTP_CLIENT",
);

ReactDOM.render(
  <React.StrictMode>
    <Provider store={getStore(httpClientKind)}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById("root"),
);
