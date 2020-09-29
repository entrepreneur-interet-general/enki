import { Store } from "@reduxjs/toolkit";
import { RootState } from "../setup/root.reducer";

export const buildExpectStateToEqual = (store: Store<RootState>) => (
  expectedState: RootState,
) => {
  expect(store.getState()).toEqual(expectedState);
};

export type ExpectStateToEqual = ReturnType<typeof buildExpectStateToEqual>;
