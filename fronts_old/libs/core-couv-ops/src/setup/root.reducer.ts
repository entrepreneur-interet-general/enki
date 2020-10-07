import { combineReducers } from "@reduxjs/toolkit";
import { helloSapeurReducer } from "../useCases/helloSapeur/helloSapeur.slice";

export const rootReducer = combineReducers({
  helloSapeur: helloSapeurReducer,
});

export type RootState = ReturnType<typeof rootReducer>;
