import { PIGGY_ALPHABET, PIGGY_ALPHABET_LENGTH } from "../constants";

export class TextService {
  findMostFrequentBigramsInText(text: string) {
    return this.getBigrams(text)
      .map((bigram) => {
        return {
          frequency: this.findBigramFrequency(text, bigram),
          bigram,
        };
      })
      .sort((a, b) => b.frequency - a.frequency)
      .slice(0, 5);
  }

  getBigrams(text: string) {
    const bigrams = text.split("").map((x, index) => x + text[index + 1]);
    bigrams.pop();
    return [...new Set(bigrams)];
  }

  findBigramsAmount(text: string) {
    return text.length - 1;
  }

  findBigramFrequency(text: string, bigram: string) {
    const bigramMatchesAmount = Array.from(
      text.matchAll(new RegExp(bigram, "g"))
    ).length;

    return bigramMatchesAmount / this.findBigramsAmount(text);
  }

  findLettersFrequencyInText(text: string) {
    return this.getLettersUsedInText(text)
      .map((letter) => {
        return {
          frequency: this.findLetterFrequency(text, letter),
          letter,
        };
      })
      .sort((a, b) => b.frequency - a.frequency);
  }

  getLettersUsedInText(text: string) {
    return [...new Set(text.split(""))];
  }

  findLetterFrequency(text: string, letter: string) {
    const letterMatchesAmount = Array.from(
      text.matchAll(new RegExp(letter, "g"))
    ).length;

    return letterMatchesAmount / text.length;
  }

  findLetterPosition(letter: string) {
    return PIGGY_ALPHABET.indexOf(letter);
  }

  findLetterByPosition(position: number) {
    return PIGGY_ALPHABET[position];
  }

  convertBigramToNumber(x: number, y: number) {
    return x * PIGGY_ALPHABET_LENGTH + y;
  }

  convertBigramToPairsOfNumber(bigram: string) {
    return [
      this.findLetterPosition(bigram[0]),
      this.findLetterPosition(bigram[1]),
    ];
  }

  convertNumbersToBigram(bigramNumber: number) {
    const a = Math.floor(bigramNumber / PIGGY_ALPHABET_LENGTH);
    const b = bigramNumber % PIGGY_ALPHABET_LENGTH;

    return this.findLetterByPosition(a) + this.findLetterByPosition(b);
  }

  findAllCombinations<T>(arr: T[]) {
    const result: T[][] = [];

    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length; j++) {
        if (
          !result.find((el) => el[0] === arr[j] && el[1] === arr[i]) &&
          arr[i] !== arr[j]
        ) {
          result.push([arr[i], arr[j]]);
        }
      }
    }

    return result;
  }

  findAllCombinationsOfTwoArrays(arr1: string[][], arr2: string[][]) {
    const cartesian = (...a: any) =>
      a.reduce((a: any, b: any) =>
        a.flatMap((d: any) => b.map((e: any) => [d, e]))
      );

    return cartesian(arr1, arr2);
  }
}
