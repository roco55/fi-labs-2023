import {
  MOST_FREQUENT_BIGRAMS_IN_PIGGY_LANGUAGE,
  PIGGY_ALPHABET_LENGTH,
} from "../constants";
import { mod } from "../util/mod";
import { NumericService } from "./numeric.service";
import { SpeechRecognizerService } from "./speech-recognizer.service";
import { TextService } from "./text.service";

export class CipherService {
  private readonly numericService = new NumericService();
  private readonly textService = new TextService();
  private readonly speechRecognizerService = new SpeechRecognizerService();

  constructor(private readonly text: string) {}

  affineDecipher(a: number, b: number) {
    let decipheredText = "";
    const n = PIGGY_ALPHABET_LENGTH * PIGGY_ALPHABET_LENGTH;

    for (let i = 0; i < this.text.length - 1; i++) {
      const bigram = this.textService.convertBigramToPairsOfNumber(
        this.text[i] + this.text[i + 1]
      );

      const bigramNumber = this.textService.convertBigramToNumber(
        bigram[0],
        bigram[1]
      );

      const inverseA = this.numericService.getInverseModulo(a, n)!;
      const decipheredBigram = mod(inverseA * (bigramNumber - b), n);

      decipheredText +=
        this.textService.convertNumbersToBigram(decipheredBigram);
    }

    return decipheredText;
  }

  findA(Y: number[], X: number[]) {
    const n = PIGGY_ALPHABET_LENGTH * PIGGY_ALPHABET_LENGTH;

    const a = mod(X[0] - X[1], n);
    const b = mod(Y[0] - Y[1], n);

    return this.numericService.solveModuloComparison(a, b, n);
  }

  findB(Y: number, a: number, X: number) {
    const n = PIGGY_ALPHABET_LENGTH * PIGGY_ALPHABET_LENGTH;
    return mod(Y - a * X, n);
  }

  getAllPosibleKeys() {
    const combinationsOfLanguageBigrams = this.textService.findAllCombinations(
      MOST_FREQUENT_BIGRAMS_IN_PIGGY_LANGUAGE
    );

    const combinationsOfCipherBigrams = this.textService.findAllCombinations(
      this.textService
        .findMostFrequentBigramsInText(this.text)
        .map((el) => el.bigram)
    );

    const allCombinations = this.textService.findAllCombinationsOfTwoArrays(
      combinationsOfCipherBigrams, combinationsOfLanguageBigrams
    );

    const keys = allCombinations.map((combination: string[][]) => {
        let x1: any = this.textService.convertBigramToPairsOfNumber(combination[1][0]);
        x1 = this.textService.convertBigramToNumber(x1[0], x1[1]);
        let x2: any = this.textService.convertBigramToPairsOfNumber(combination[1][1]);
        x2 = this.textService.convertBigramToNumber(x2[0], x2[1]);

        let y1: any = this.textService.convertBigramToPairsOfNumber(combination[0][0]);
        y1 = this.textService.convertBigramToNumber(y1[0], y1[1]);
        let y2: any = this.textService.convertBigramToPairsOfNumber(combination[0][1]);
        y2 = this.textService.convertBigramToNumber(y2[0], y2[1]);

        let a = this.findA([x1, x2], [y1, y2]);

        if(a instanceof Array<number>){
            a = a[0];
        }

        if(!a){
            return [];
        }

        const b = this.findB(x1, <number>a, y1);

        return [a, b];
    });

    return keys;
  }

  decipherText(){
    const keys = this.getAllPosibleKeys();

    for(let i = 0; i < keys.length; i++){
        if(keys[i].length){
            const decipheredText = this.affineDecipher(keys[i][1], keys[i][0]);
            if(this.speechRecognizerService.isTextSimilarToPigVoice(decipheredText, 3)){
                console.log(decipheredText);
                break;
            }
        }
    }
  }
}
