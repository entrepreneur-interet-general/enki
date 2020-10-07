import { HttpClient } from "../ports/HttpClient";

const wait = (delay: number) =>
  new Promise((resolve) => setTimeout(resolve, delay));

export class InMemoryHttpClient implements HttpClient {
  public async helloSapeur(): Promise<string> {
    if (this.requestsDelay) await wait(this.requestsDelay);
    if (this.error) throw new Error(this.error);
    return this.message;
  }

  private message: string = "Initial Hello Sapeur msg from InMemory Adapter !";
  private error?: string;

  constructor(private requestsDelay?: number) {}

  public setMessage(message: string) {
    this.message = message;
  }

  public setError(errorMessage: string) {
    this.error = errorMessage;
  }
}
