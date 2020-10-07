import { add } from "@fronts/utilities";
import { actions, RootState } from "@fronts/core-couv-ops";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import "./app.css";

export const App = () => {
  const message = useSelector((state: RootState) => state.helloSapeur.message);
  const isFetching = useSelector(
    (state: RootState) => state.helloSapeur.isFetching,
  );
  const dispatch = useDispatch();

  return (
    <div className="app">
      <header>
        <h1>Welcome ! {add(8, 2)}</h1>
        <p>
          Message: {message ? <strong>{message}</strong> : "No message yet..."}
        </p>
        <p>{isFetching ? "Loading..." : ""}</p>
      </header>

      <button onClick={() => dispatch(actions.helloSapeurThunk)}>
        Get message
      </button>
    </div>
  );
};
