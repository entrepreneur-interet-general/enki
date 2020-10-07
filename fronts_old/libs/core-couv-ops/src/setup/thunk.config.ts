import { Action, ThunkAction } from "@reduxjs/toolkit";
import { HttpClient } from "../ports/HttpClient";
import { RootState } from "../setup/root.reducer";

export type Dependencies = {
  httpClient: HttpClient;
};

export type AppThunk = ThunkAction<
  void,
  RootState,
  Dependencies,
  Action<string>
>;
