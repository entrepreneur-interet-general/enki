import { AppThunk } from "../../setup/thunk.config";
import { helloSapeurActions } from "./helloSapeur.slice";

export const helloSapeurThunk: AppThunk = async (
  dispatch,
  _,
  { httpClient },
) => {
  dispatch(helloSapeurActions.helloSapeurRequested());
  try {
    const helloSapeurMessage = await httpClient.helloSapeur();
    dispatch(helloSapeurActions.helloSapeurFetched(helloSapeurMessage));
  } catch (e) {
    dispatch(helloSapeurActions.helloSapeurFailed(e.message));
  }
};
