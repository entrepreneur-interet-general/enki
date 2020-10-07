import { configureStore, getDefaultMiddleware } from "@reduxjs/toolkit";
import { rootReducer } from "./root.reducer";
import { Dependencies } from "./thunk.config";

export const configureReduxStore = (dependencies: Dependencies) =>
  configureStore({
    reducer: rootReducer,
    middleware: getDefaultMiddleware({
      thunk: {
        extraArgument: dependencies,
      },
    }),
  });
