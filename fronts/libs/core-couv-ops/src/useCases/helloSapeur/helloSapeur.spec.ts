import { Store, ThunkDispatch } from "@reduxjs/toolkit";

import { InMemoryHttpClient } from "../../secondaryAdapters/InMemoryHttpClient";
import { RootState } from "../../setup/root.reducer";
import { configureReduxStore } from "../../setup/store.config";
import {
  buildExpectStateToEqual,
  ExpectStateToEqual,
} from "../../utils/test.utils";
import { helloSapeurActions } from "./helloSapeur.slice";
import { helloSapeurThunk } from "./helloSapeur.thunk";

describe("Hello sapeur", () => {
  let store: Store<RootState>;
  let expectStateToEqual: ExpectStateToEqual;
  let httpClient: InMemoryHttpClient;

  beforeEach(() => {
    httpClient = new InMemoryHttpClient();
    store = configureReduxStore({ httpClient });
    expectStateToEqual = buildExpectStateToEqual(store);
  });

  describe("Fetching hello sapeur ", () => {
    it("Indicates when fetching is ongoing", () => {
      store.dispatch(helloSapeurActions.helloSapeurRequested());
      expectStateToEqual({ helloSapeur: { isFetching: true } });
    });
    describe("When all is good", () => {
      it("Retrieves the hello sapeur message", async () => {
        const expectedValue = "Hello Sapeur expected !";
        httpClient.setMessage(expectedValue);
        await fetchHelloSapeur();

        expectStateToEqual({
          helloSapeur: { message: expectedValue, isFetching: false },
        });
      });
    });
    describe("When something wrong happens", () => {
      it("gets the error message", async () => {
        const errorMessage = "My expected error !";
        httpClient.setError(errorMessage);
        await fetchHelloSapeur();
        expectStateToEqual({
          helloSapeur: {
            isFetching: false,
            error: errorMessage,
          },
        });
      });
    });
  });

  const fetchHelloSapeur = async () =>
    (store.dispatch as ThunkDispatch<RootState, any, any>)(helloSapeurThunk);
});
