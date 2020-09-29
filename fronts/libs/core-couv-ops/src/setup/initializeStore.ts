import { FlaskHttpClient } from "../secondaryAdapters/FlaskHttpClient";
import { InMemoryHttpClient } from "../secondaryAdapters/InMemoryHttpClient";
import { configureReduxStore } from "./store.config";

export const getStore = (httpClientKind: "IN_MEMORY" | "FLASK") => {
  const httpClient =
    httpClientKind === "IN_MEMORY"
      ? new InMemoryHttpClient(500)
      : new FlaskHttpClient();

  return configureReduxStore({ httpClient });
};
