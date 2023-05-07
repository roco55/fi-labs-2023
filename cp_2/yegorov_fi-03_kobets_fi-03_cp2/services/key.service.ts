import { TextService } from "./index";
import {
  MAX_KEY_LENGTH,
  MOST_FREQUENT_LETTER_POSITION_IN_PIGGY_LANGUAGE,
  THEORETICAL_KEY_VALUE,
} from "../constants";
import { mod } from "../util";

export class KeyService {
  private readonly alphabetLength: number = this.alphabet.length;
  private readonly textService = new TextService(this.alphabet);

  constructor(private readonly alphabet: string) {}

  calculateMatchingIndex(text: string) {
    if (text.length === 1) {
      return 0;
    }

    const sum = this.alphabet
      .split("")
      .reduce(
        (acc, letter) =>
          acc +
          this.textService.letterAmountInText(text, letter) *
            (this.textService.letterAmountInText(text, letter) - 1),
        0
      );

    return sum / (text.length * (text.length - 1));
  }

  findKeyLength(text: string) {
    const theoreticalValue = THEORETICAL_KEY_VALUE;

    const result: {
      r: number;
      i: number;
    }[] = [];

    for (let r = 2; r <= MAX_KEY_LENGTH; r++) {
      const splittedText = this.textService.splitTextToGroups(text, r);
      const matchingIndexes = splittedText.map((text) =>
        this.calculateMatchingIndex(text)
      );

      const mean =
        matchingIndexes.reduce((acc, index) => acc + index, 0) /
        matchingIndexes.length;

      result.push({
        r,
        i: mean,
      });
    }

    const filteredValues = result.sort((a, b) => {
      if (Math.abs(a.i - theoreticalValue) < Math.abs(b.i - theoreticalValue)) {
        return -1;
      } else if (
        Math.abs(a.i - theoreticalValue) > Math.abs(b.i - theoreticalValue)
      ) {
        return 1;
      } else {
        return 0;
      }
    });

    return filteredValues[0].r;
  }

  findKeySymbolsInnacurate(keyLength: number, text: string) {
    const mostFrequentLetterPosition =
      MOST_FREQUENT_LETTER_POSITION_IN_PIGGY_LANGUAGE;
    const blocks = this.textService.splitTextToGroups(text, keyLength);

    const mostFrequentLetterInBlocks = blocks
      .map((block) =>
        this.alphabet.split("").map((letter) => {
          return {
            amount: this.textService.letterAmountInText(block, letter),
            letter,
          };
        })
      )
      .map((block) => block.sort((a, b) => b.amount - a.amount))
      .map((block, index) => {
        return { ...block[0], block: index };
      });

    const mostFrequentLetterInBlocksPositions = mostFrequentLetterInBlocks.map(
      (block) => {
        return this.textService.convertLetterToPosition(block.letter);
      }
    );

    const arrayOfKPositions = mostFrequentLetterInBlocksPositions.map(
      (position) =>
        mod(position - mostFrequentLetterPosition, this.alphabetLength)
    );

    return this.textService.convertPositionsToSymbols(arrayOfKPositions);
  }

  findKeySymbolsAccurate(keyLength: number, text: string) {
    const blocks = this.textService.splitTextToGroups(text, keyLength);
    const keySymbolsPositions: number[] = [];

    for (let i = 0; i < blocks.length; i++) {
      let maxMValue = 0;

      for (let g = 0; g < this.alphabet.length; g++) {
        let currentMValue = 0;

        for (let t = 0; t < this.alphabet.length; t++) {
          const p = this.textService.getLetterFrequencyInLanguage(
            this.textService.convertPositionToLetter(t)
          );

          const N = this.textService.letterAmountInText(
            blocks[i],
            this.textService.convertPositionToLetter(
              (t + g) % this.alphabet.length
            )
          );

          currentMValue += p * N;
        }

        if (currentMValue > maxMValue) {
          maxMValue = currentMValue;
          keySymbolsPositions[i] = g;
        }
      }
    }

    return this.textService.convertPositionsToSymbols(keySymbolsPositions);
  }
}
