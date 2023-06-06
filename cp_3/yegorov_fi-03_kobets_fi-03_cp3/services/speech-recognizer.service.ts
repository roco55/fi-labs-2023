import { LETTERS_FREQUENCY_IN_PIG_LANGUAGE } from "../constants";
import { TextService } from "./text.service";

export class SpeechRecognizerService {
  private readonly textService = new TextService();

  isTextSimilarToPigVoice(text: string, error: number) {
    const lettersFrequency = this.textService.findLettersFrequencyInText(text);
    const fiveMostFrequentInText = lettersFrequency
      .slice(0, 5)
      .map((x) => x.letter);

    const fiveMostFrequentInLanguage: string[] = [];

    let i = 0;

    for (const letter in LETTERS_FREQUENCY_IN_PIG_LANGUAGE) {
      fiveMostFrequentInLanguage.push(letter);
      i++;

      if(i === 5){
        break;
      }
    }

    let recognitionCount = 0;

    fiveMostFrequentInText.forEach((letter) => {
      if(fiveMostFrequentInLanguage.includes(letter)){
        recognitionCount++;
      }
    });

    return recognitionCount >= error;
  }
}
