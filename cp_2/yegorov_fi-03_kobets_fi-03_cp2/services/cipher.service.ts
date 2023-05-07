import { FileService, KeyService, TextService } from "./index";
import { mod } from "../util";


export class CipherService {
  private readonly textService = new TextService(this.alphabet);
  private readonly keyService = new KeyService(this.alphabet);
  private readonly fileService = new FileService(this.textUrl);
  private readonly alphabetLength = this.alphabet.length;
  private readonly text: string;

  constructor(private readonly alphabet: string, private readonly textUrl: string) {
    this.text = this.fileService.getPreparedText();
  }

  vigenereCipher(key: string) {
    const keyPositions = this.textService.convertSymbolsToPositions(key);
    const textPositions = this.textService.convertSymbolsToPositions(this.text);

    const cipheredTextPositions = textPositions.map((position, index) =>
      mod(position + keyPositions[index % key.length], this.alphabetLength)
    );

    return this.textService.convertPositionsToSymbols(cipheredTextPositions);
  }

  vigenereDecipher(key: string) {
    const keyPositions = this.textService.convertSymbolsToPositions(key);
    const textPositions = this.textService.convertSymbolsToPositions(this.text);

    const decipheredTextPositions = textPositions.map((position, index) =>
      mod(position - keyPositions[index % key.length], this.alphabetLength)
    );

    return this.textService.convertPositionsToSymbols(decipheredTextPositions);
  }

  breakVigener(){
    const keyLength = this.keyService.findKeyLength(this.text);
    const keyInaccurate = this.keyService.findKeySymbolsInnacurate(keyLength, this.text);
    const keyAccurate = this.keyService.findKeySymbolsAccurate(keyLength, this.text);

    return [keyInaccurate, keyAccurate];
  }
}
