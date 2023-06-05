import java.io.*;
import java.util.*;

public class Tools {

    private static final String ALPHABET = "абвгдежзийклмнопрстуфхцчшщыьэюя";
    private static final String FILE_PATH = "cp_3/medvedtskyi-fi-04-skovron-fi-04-cp3/src/to_decode.txt";
    private final List<String> MostFrequencyBiGrams = new ArrayList<>(Arrays.asList("то", "ст", "на", "но", "ен"));
    private final List<String> BiGrams = new ArrayList<>();
    private static final double[] lettersFrequency = new double[]{0.0792, 0.0171, 0.0433, 0.0174, 0.0305, 0.0841, 0.0105, 0.0175, 0.0683, 0.0112, 0.0336, 0.0500, 0.0326, 0.0672, 0.1108, 0.0281, 0.0445, 0.0533, 0.0618, 0.0280, 0.0019, 0.0089, 0.0036, 0.0147, 0.0081, 0.0037, 0.0002, 0.0194, 0.0038, 0.0061, 0.0213};
    private double I = 0;
    private static final int M = ALPHABET.length() * ALPHABET.length();

    Tools() {
        for (int i = 0; i < ALPHABET.length(); i++) {
            for (int j = 0; j < ALPHABET.length(); j++) {
                BiGrams.add(("" + ALPHABET.charAt(i) + ALPHABET.charAt(j)));
            }
        }
        for (double v : lettersFrequency) {
            I += v * v;
        }
    }

    public void run() throws Exception {
        String text = getText(FILE_PATH);
        List<List<Integer>> keys = getKeys(getFirst5Elements(calculateBigrams(text)));
        Map<Double, List<Integer>> keyRatings = new TreeMap<>(Collections.reverseOrder());
        for (List<Integer> key : keys) {
            String decryptedText = decrypt(text, key);
            if (decryptedText.equals("Invalid key")) continue;
            double rating = getIndex(decryptedText);
            keyRatings.put(rating, key);
        }
        int numOfKeys = 0;
        for (Map.Entry<Double, List<Integer>> entry : keyRatings.entrySet()) {
            if (numOfKeys == 10) break;
            System.out.println(entry.getKey() + ": " + entry.getValue());
            numOfKeys++;
        }
        List<Integer> k = new ArrayList<>();
        k.add(703);
        k.add(956);
        System.out.println(decrypt(text, k));
    }

    private int[] gcd(int a, int b) {
        int r0 = a, r1 = b, u0 = 1, u1 = 0, v0 = 0, v1 = 1;
        while (r1 != 0) {
            int q = r0 / r1;
            int temp_r0 = r0, temp_r1 = r1;
            r0 = r1;
            r1 = temp_r0 - q * temp_r1;
            int temp_u0 = u0, temp_u1 = u1;
            u0 = u1;
            u1 = temp_u0 - q * temp_u1;
            int temp_v0 = v0, temp_v1 = v1;
            v0 = v1;
            v1 = temp_v0 - q * temp_v1;
        }
        return new int[]{r0, u0, v0};
    }

    private List<Integer> solveLinearCongruence(int a, int b, int m) {
        List<Integer> solutions = new ArrayList<>();
        a %= m;
        b %= m;
        int aInv = (gcd(a, m)[1] + m) % m, d = gcd(a, m)[0];
        if (d == 1) {
            solutions.add((aInv * b) % m);
            return solutions;
        }
        if (b % d == 0) {
            int a1 = a / d, b1 = b / d, m1 = m / d;
            int a1Inv = (gcd(a1, m1)[1] + m1) % m1;
            int x0 = (a1Inv * b1) % m1;
            for (int i = 0; i < d; i++) {
                solutions.add(x0 + i * m1);
            }
        }
        return solutions;
    }

    private List<List<Integer>> getKeys(List<String> firstFiveBiGrams) {
        List<List<Integer>> keys = new ArrayList<>();
        for (int i1 = 0; i1 < 5; i1++) {
            for (int j1 = 0; j1 < 5; j1++) {
                for (int i2 = 0; i2 < 5; i2++) {
                    for (int j2 = 0; j2 < 5; j2++) {
                        if ((i1 == i2) || (j1 == j2)) continue;
                        int x1 = BiGrams.indexOf(MostFrequencyBiGrams.get(i1)), x2 = BiGrams.indexOf(MostFrequencyBiGrams.get(i2));
                        int y1 = BiGrams.indexOf(firstFiveBiGrams.get(j1)), y2 = BiGrams.indexOf(firstFiveBiGrams.get(j2));
                        List<Integer> solutions = solveLinearCongruence((x1 - x2 + M) % M, (y1 - y2 + M) % M, M);
                        for (Integer solution : solutions) {
                            List<Integer> key = new ArrayList<>();
                            key.add(solution);
                            key.add((y1 - solution * x1 + M * M) % M);
                            keys.add(key);
                        }
                    }
                }
            }
        }
        return keys;
    }

    private Map<String, Integer> calculateBigrams(String text) {
        Map<String, Integer> bigram = new TreeMap<>();

        for (int i = 0; i < text.length() - 1; i += 2) {
            char c1 = text.charAt(i);
            char c2 = text.charAt(i + 1);
            String temp = c1 + String.valueOf(c2);

            if (!bigram.containsKey(temp)) {
                bigram.put(temp, 1);
            } else {
                int n = bigram.get(temp);
                bigram.put(temp, (n + 1));
            }
        }

        List<Map.Entry<String, Integer>> listForSort = new ArrayList<>(bigram.entrySet());
        listForSort.sort(Map.Entry.comparingByValue(Comparator.reverseOrder()));

        Map<String, Integer> sortedBigram = new LinkedHashMap<>();
        for (Map.Entry<String, Integer> entry : listForSort) {
            sortedBigram.put(entry.getKey(), entry.getValue());
        }

        return sortedBigram;
    }

    private String getText(String filepath) throws IOException {
        InputStream file = new FileInputStream(filepath);
        StringBuilder resultStringBuilder = new StringBuilder();

        try (BufferedReader br = new BufferedReader(new InputStreamReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                resultStringBuilder.append(line).append("\n");
            }
        }

        String temp = resultStringBuilder.toString();
        temp = temp.replaceAll("\n", "");

        return temp;
    }

    private List<String> getFirst5Elements(Map<String, Integer> map) {
        int numOfMaps = 0;
        List<String> bigrams = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            if (numOfMaps == 5) break;
            bigrams.add(entry.getKey());
            numOfMaps++;
        }
        return bigrams;
    }

    private String decryptBiGram(String bigram, int aInv, int b) {
        return BiGrams.get((aInv * (BiGrams.indexOf(bigram) - b + (ALPHABET.length() * ALPHABET.length())) ) % (ALPHABET.length() * ALPHABET.length()));
    }

    private String decrypt(String encryptedText, List<Integer> key) {
        int a = key.get(0), b = key.get(1);
        int d = gcd(a, M)[0], aInv = (gcd(a, M)[1] + M) % M;
        if (d != 1) {
            return "Invalid key";
        }
        StringBuilder result = new StringBuilder();
        for (int i = 1; i < encryptedText.length(); i += 2) {
            result.append(decryptBiGram("" + encryptedText.charAt(i-1) + encryptedText.charAt(i), aInv, b));
        }
        return result.toString();
    }

    private Map<Character, Integer> calcLetters(String input) {
        Map<Character, Integer> letters = new HashMap<>();

        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            if (!letters.containsKey(c)) {
                letters.put(c, 1);
            } else {
                int n = letters.get(c);
                letters.put(c, (n + 1));
            }
        }

        List<Map.Entry<Character, Integer>> listForSort = new ArrayList<>(letters.entrySet());
        listForSort.sort(Map.Entry.comparingByValue(Comparator.reverseOrder()));

        Map<Character, Integer> sortedLetters = new LinkedHashMap<>();
        for (Map.Entry<Character, Integer> entry : listForSort) {
            sortedLetters.put(entry.getKey(), entry.getValue());
        }

        return sortedLetters;
    }

    private double getIndex(String text) {
        Map<Character, Integer> letters =  new HashMap<>(calcLetters(text));
        double sum = 0;
        for (int i = 0; i < ALPHABET.length(); i++) {
            sum += (double) (letters.get(ALPHABET.charAt(i)) * (letters.get(ALPHABET.charAt(i)) - 1)) / (text.length() * (text.length() - 1));
        }
        return sum;
    }
}
