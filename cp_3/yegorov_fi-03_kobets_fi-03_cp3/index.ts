import { FILE } from "./constants";
import { CipherService, FileService } from "./services";


const fileService = new FileService(FILE);
const text = fileService.getText();
const cipherService = new CipherService(text);

