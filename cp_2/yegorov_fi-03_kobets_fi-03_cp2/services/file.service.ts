import * as fs from "fs";
import { RUSSIAN_PIG_REGEXP } from "../constants";

export class FileService {
  private fileData = "";

  constructor(private readonly fileUrl: string) {}

  getPreparedText() {
    this.fileData = fs.readFileSync(this.fileUrl, {
      encoding: "utf-8",
      flag: "r",
    });
    this.fileData = this.fileData.replace(RUSSIAN_PIG_REGEXP, "").toLowerCase();
    return this.fileData;
  }
}
