import Axios from "axios";
import { HttpClient } from "../ports/HttpClient";

const NX_BACKEND_URL = "http://localhost:5000";

export class FlaskHttpClient implements HttpClient {
  public async helloSapeur(): Promise<string> {
    return Axios.get(NX_BACKEND_URL);
  }
}
