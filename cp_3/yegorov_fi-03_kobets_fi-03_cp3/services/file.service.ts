import * as fs from "fs";

export class FileService {
  constructor(private readonly fileUrl: string) {}

  getText() {
    return fs.readFileSync(this.fileUrl, {
      encoding: "utf-8",
      flag: "r",
    });
  }
}
