import { LETTERS_FREQUENCY_IN_PIG_LANGUAGE } from "../constants";

export class TextService {
  constructor(private readonly alphabet: string) {}

  convertSymbolsToPositions(text: string) {
    return text.split("").map((letter) => this.alphabet.indexOf(letter));
  }

  convertPositionsToSymbols(positions: number[]) {
    return positions.map((position) => this.alphabet[position]).join("");
  }

  convertLetterToPosition(letter: string) {
    return this.alphabet.indexOf(letter);
  }

  convertPositionToLetter(position: number) {
    return this.alphabet[position];
  }

  letterAmountInText(text: string, letter: string) {
    return Array.from(text.matchAll(new RegExp(letter, "g"))).length;
  }

  findLetterFrequencyInText(text: string, letter: string) {
    return this.letterAmountInText(text, letter) / text.length;
  }

  getLetterFrequencyInLanguage(letter: string){
    return LETTERS_FREQUENCY_IN_PIG_LANGUAGE[letter];
  }

  splitTextToGroups(text: string, groupsAmount: number) {
    const result: string[] = [];

    for (let i = 0; i < groupsAmount; i++) {
      const temp: string[] = [];

      for (let j = 0; j < text.length; j++) {
        if (j % groupsAmount === i) {
          temp.push(text[j]);
        }
      }

      result.push(temp.join(""));
    }

    return result;
  }
}
