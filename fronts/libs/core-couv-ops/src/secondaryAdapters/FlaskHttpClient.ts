import Axios from "axios";
import { HttpClient } from "../ports/HttpClient";

export class FlaskHttpClient implements HttpClient {
  constructor(private backendUrl: string) {}

  public async helloSapeur(): Promise<string> {
    const response = await Axios.get(this.backendUrl);
    return response.data.message;
  }
}
