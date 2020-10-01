import { createSlice, PayloadAction } from "@reduxjs/toolkit";

type HelloSapeurState = {
  message?: string;
  isFetching: boolean;
  error?: string;
};

const initialState: HelloSapeurState = {
  isFetching: false,
};

const helloSapeurSlice = createSlice({
  name: "helloSapeur",
  initialState,
  reducers: {
    helloSapeurRequested: (state) => ({ ...state, isFetching: true }),
    helloSapeurFetched: (
      state,
      action: PayloadAction<string>,
    ): HelloSapeurState => ({
      ...state,
      isFetching: false,
      message: action.payload,
    }),
    helloSapeurFailed: (
      state,
      action: PayloadAction<string>,
    ): HelloSapeurState => ({
      ...state,
      isFetching: false,
      error: action.payload,
    }),
  },
});

export const {
  reducer: helloSapeurReducer,
  actions: helloSapeurActions,
} = helloSapeurSlice;
