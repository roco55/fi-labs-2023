import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class Tools {
    private static final String symbols = "абвгдежзийклмнопрстуфхцчшщъыьэюя";
    private static final String FILE_PATH_TO_ENCODE = "cp_2/medvedtskyi-fi-04-skovron-fi-04-cp2/src/windows_license.txt";
    private static final String FILE_PATH_TO_DECODE = "cp_2/medvedtskyi-fi-04-skovron-fi-04-cp2/src/to_decode.txt";
    private static final int keyLength = 17;
    private final Map<Character, Double> letterFrequency;

    public Tools(){
        letterFrequency = new HashMap<>();
        letterFrequency.put('о', 0.11540391238792298);
        letterFrequency.put('е', 0.08236945108644807);
        letterFrequency.put('а', 0.08190993805712148);
        letterFrequency.put('и', 0.06786302508392858);
        letterFrequency.put('н', 0.06479264256979181);
        letterFrequency.put('т', 0.05861445507890265);
        letterFrequency.put('с', 0.05329828966291499);
        letterFrequency.put('л', 0.050160459687087294);
        letterFrequency.put('в', 0.04626808843014945);
        letterFrequency.put('р', 0.04428339247677958);
        letterFrequency.put('к', 0.033624517805042026);
        letterFrequency.put('д', 0.030659005215211796);
        letterFrequency.put('м', 0.029640766116135826);
        letterFrequency.put('у', 0.02722136039354506);
        letterFrequency.put('п', 0.026334970203452004);
        letterFrequency.put('я', 0.022014416351005293);
        letterFrequency.put('г', 0.019695964248493854);
        letterFrequency.put('ь', 0.01949057584902212);
        letterFrequency.put('ы', 0.019370040707806718);
        letterFrequency.put('б', 0.017395788232376086);
        letterFrequency.put('з', 0.017139052733036418);
        letterFrequency.put('ч', 0.014454643757737421);
        letterFrequency.put('й', 0.011201935524578073);
        letterFrequency.put('ж', 0.010659744961565826);
        letterFrequency.put('ш', 0.009276854424444701);
        letterFrequency.put('х', 0.008606731256676754);
        letterFrequency.put('ю', 0.006139024448617001);
        letterFrequency.put('ц', 0.0036029998890380467);
        letterFrequency.put('э', 0.0030677716446519602);
        letterFrequency.put('щ', 0.002962901720345418);
        letterFrequency.put('ф', 0.0020482271108335855);
        letterFrequency.put('ъ', 0.0004290528853371394);
    }

    public void run() throws IOException {
        PrintStream out = new PrintStream(new FileOutputStream("output.txt"));
        System.setOut(out);

        String key2 = generateKey(2);
        String key3 = generateKey(3);
        String key4 = generateKey(4);
        String key5 = generateKey(5);
        String key10 = generateKey(10);

        String openText = filter(FILE_PATH_TO_ENCODE);
        String encodedByKey2 = encode(openText, key2);
        String encodedByKey3 = encode(openText, key3);
        String encodedByKey4 = encode(openText, key4);
        String encodedByKey5 = encode(openText, key5);
        String encodedByKey10 = encode(openText, key10);

        String EncodedText = filter(FILE_PATH_TO_DECODE);

        System.out.println("Open text:");
        System.out.println(openText);
        System.out.println();
        System.out.println("Кey 1: " + key2);
        System.out.println(encodedByKey2);
        System.out.println("Key 2: " + key3);
        System.out.println(encodedByKey3);
        System.out.println("Key 3: " + key4);
        System.out.println(encodedByKey4);
        System.out.println("Key 4: " + key5);
        System.out.println(encodedByKey5);
        System.out.println("Key 5: " + key10);
        System.out.println(encodedByKey10);
        System.out.println();

        System.out.println("I (key 1) = " + calculateI(encodedByKey2));
        System.out.println("I (key 2) = " + calculateI(encodedByKey3));
        System.out.println("I (key 3) = " + calculateI(encodedByKey4));
        System.out.println("I (key 4) = " + calculateI(encodedByKey5));
        System.out.println("I (key 5) = " + calculateI(encodedByKey10));
        System.out.println();

        System.out.println("Length of key:");
        calculateKeyLength(EncodedText).forEach((key, value) -> System.out.println(key + ": " + value));

        System.out.println("Key:");
        System.out.println(findKey(EncodedText));
        System.out.println("Key via M");
        System.out.println(findKeyViaM(EncodedText));

        System.out.println("Decoded with first key:");
        System.out.println(decode(EncodedText, findKey(EncodedText)));

        System.out.println("Decoded with second key:");
        System.out.println(decode(EncodedText, findKeyViaM(EncodedText)));
        out.close();
    }

    private String filter(String filePath) throws IOException {
        InputStream srcFile = new FileInputStream(filePath);
        String temp = readFromInputStream(srcFile);

        temp = temp.replaceAll("ё", "e");
        temp = temp.replaceAll("[^^а-яА-Я]", "");
        temp = temp.replaceAll("\n", "");
        temp = temp.toLowerCase();

        return temp;
    }

    private String readFromInputStream(InputStream inputStream) throws IOException {
        StringBuilder resultStringBuilder = new StringBuilder();

        try (BufferedReader br = new BufferedReader(new InputStreamReader(inputStream))) {
            String line;

            while ((line = br.readLine()) != null) {
                resultStringBuilder.append(line).append("\n");
            }
        }

        return resultStringBuilder.toString();
    }

    private String encode(String text, String key) {
        int indexInKey = 0;
        StringBuilder builder = new StringBuilder(text.length());

        for (int i = 0; i < text.length(); i++) {
            builder.append(symbols.charAt(((symbols.indexOf(text.charAt(i)) + 1) + (symbols.indexOf(key.charAt(indexInKey)) + 1) - 1) % 32));
            indexInKey += 1;
            indexInKey = indexInKey % key.length();
        }

        return builder.toString();
    }

    private String generateKey(Integer length) {
        Random random = new Random();
        StringBuilder builder = new StringBuilder(length);

        for (int i = 0; i < length; i++) {
            int index = random.nextInt(symbols.length());
            builder.append(symbols.charAt(index));
        }

        return builder.toString();
    }

    private float calculateI(String text) {
        Map<Character, Integer> letters = calcLetters(text);
        float sum = 0;
        for (Integer value : letters.values()) {
            sum += ((float)value * ((float)value - 1));
        }
        return (float) (sum / (text.length() * (text.length() - 1)));
    }

    private Map<Integer, Float> calculateKeyLength(String text) {
        Map<Integer, Float> r = new HashMap<>();
        for (int i = 2; i <= 30; i++) {
            float sum = 0;
            StringBuilder[] builders = new StringBuilder[i];
            for (int j = 0; j < i; j++) {
                builders[j] = new StringBuilder((text.length() / i));
            }
            int k = 0;
            while(k < text.length()) {
                builders[(k % i)].append(text.charAt(k));
                k++;
            }
            for (int j = 0; j < i; j++) {
                sum += calculateI(builders[j].toString());
            }
            r.put(i, (sum / i));
        }
        return r;
    }

    private String findKey(String text) {
        StringBuilder[] rows = separateText(text);
        StringBuilder key = new StringBuilder();
        for (int i = 0; i < keyLength; i++) {
            key.append(symbols.charAt((symbols.indexOf(max(calcFrequency(rows[i].toString()))) - symbols.indexOf('о') + 32) % 32));
        }
        return key.toString();
    }

    private Map<Character, Double> calcFrequency(String text) {
        Map<Character, Integer> characters = calcLetters(text);
        Map<Character, Double> frequency = new HashMap<>();
        characters.forEach((key, value) -> frequency.put(key, ((double)value / (double)text.length())));
        return frequency;
    }

    private StringBuilder[] separateText(String text) {
        StringBuilder[] rows = new StringBuilder[keyLength];
        for (int i = 0; i < keyLength; i++) {
            rows[i] = new StringBuilder();
        }
        int k = 0;
        while(k < text.length()) {
            rows[(k % keyLength)].append(text.charAt(k));
            k++;
        }
        return rows;
    }

    private Map<Character, Integer> initEmptyMap() {
        Map<Character, Integer> map = new HashMap<>();
        for (int i = 0; i < symbols.length(); i++) {
            map.put(symbols.charAt(i), 0);
        }
        return map;
    }

    private Character max(Map<Character, Double> frequency) {
        char cMax = '-';
        double dMax = 0;
        for (Map.Entry<Character, Double> entry : frequency.entrySet()) {
            if (entry.getValue() > dMax) {
                dMax = entry.getValue();
                cMax = entry.getKey();
            }
        }
        return cMax;
    }
    private String findKeyViaM(String text) {
        StringBuilder[] Y = separateText(text);
        StringBuilder key = new StringBuilder();
        for (int i = 0; i < keyLength; i++) {
            Map<Character, Integer> letters = calcLetters(Y[i].toString());
            double maxM = 0;
            int charId = 0;
            for (int g = 0; g < 32; g++) {
                double currentM = 0;
                for (int t = 0; t < 32; t++) {
                    currentM += letterFrequency.get(symbols.charAt(t)) * letters.get(symbols.charAt((t + g) % 32));
                }
                if (currentM > maxM) {
                    maxM = currentM;
                    charId = g;
                }
            }
            key.append(symbols.charAt(charId));
        }
        return key.toString();
    }
    private Map<Character, Integer> calcLetters(String text) {
        Map<Character, Integer> letters = initEmptyMap();
        for (int i = 0; i < text.length(); i++) {
            letters.put(text.charAt(i), letters.get(text.charAt(i)) + 1);
        }
        return letters;
    }
    private String decode(String text, String key) {
        StringBuilder openText = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            openText.append(symbols.charAt((symbols.indexOf(text.charAt(i)) - symbols.indexOf(key.charAt(i % key.length())) + 32) % 32));
        }
        return openText.toString();
    }

    
 }
