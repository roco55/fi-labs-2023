interface ILettersFrequency {
  [key: string]: number;
}

export const PIGGY_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя";
export const MOST_FREQUENT_LETTER_POSITION_IN_PIGGY_LANGUAGE = 14;
export const RUSSIAN_PIG_REGEXP = /[^А-Я]/gi;

export const LETTERS_FREQUENCY_IN_PIG_LANGUAGE: ILettersFrequency = {
  о: 0.1097,
  е: 0.0849,
  а: 0.0801,
  и: 0.0735,
  н: 0.067,
  т: 0.0626,
  с: 0.0547,
  р: 0.0473,
  в: 0.0454,
  л: 0.044,
  к: 0.0349,
  м: 0.0321,
  д: 0.0298,
  п: 0.0281,
  у: 0.0262,
  я: 0.0201,
  ы: 0.019,
  ь: 0.0174,
  г: 0.017,
  з: 0.0165,
  б: 0.0159,
  ч: 0.0144,
  й: 0.0121,
  х: 0.0097,
  ж: 0.0094,
  ш: 0.0073,
  ю: 0.0064,
  ц: 0.0048,
  щ: 0.0036,
  э: 0.0032,
  ф: 0.0026,
  ъ: 0.0004,
};
