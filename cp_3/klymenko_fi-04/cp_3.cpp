#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>

std::vector<std::string> langBigrams = { "ст", "но", "то", "на", "ен" };
std::vector<std::string> textBigrams = { "ще", "хе", "чв", "ле", "цв", "ощ", "сд", "же", "де", "гд", "ню", "нв", "мю", "лп" };

std::string alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя";
int m = 31;
int M = 961;
float I = 0.05492369;


std::vector<int> findGCD(int a, int b) {
    if (b == 0) {
        return { a, 1, 0 };
    }
    std::vector<int> result = findGCD(b, a % b);
    return {result[0], result[2], result[1] - (a / b) * result[2]};
}

int findInverse(int a, int mod) {
    std::vector<int> result = findGCD(a, mod);
    int gcd = result[0];
    int x = result[1];
    if (gcd == 1) {
        return x % mod;
    }
    else {
        std::cout << "no inverse" << std::endl;
        return 0;
    }
}

std::vector<int> solve_lin_eq(int a, int b, int mod) {
    a %= mod;
    b %= mod;
    std::vector<int> result = findGCD(a, mod);
    int d = result[0];
    int x = result[1];
    if (d == 1) {
        return { (x * b) % mod };
    }
    else if (b % d == 0) {
        a /= d;
        b /= d;
        mod /= d;
        x = (findInverse(a, mod) * b) % mod;
        std::vector<int> res;
        for (int k = 0; k < d; ++k) {
            res.push_back(x + k * mod);
        }
        return res;
    }
    else {
        return {};
    }
}

int numberOfBigram(const std::string& bigram) {
    int index1 = alphabet.find(bigram[0]);
    int index2 = alphabet.find(bigram[1]);
    return index1 * m + index2;
}

std::vector<std::pair<int, int>> findPair(const std::vector<std::string>& textBigrams) {
    std::vector<std::pair<int, int>> keys;
    int n = 5;
    for (int a_1 = 0; a_1 < n; ++a_1) {
        for (int b_1 = 0; b_1 < n; ++b_1) {
            for (int a_2 = 0; a_2 < n; ++a_2) {
                for (int b_2 = 0; b_2 < n; ++b_2) {
                    if (a_1 == a_2 || b_1 == b_2) {
                        continue;
                    }

                    int a1 = numberOfBigram(langBigrams[a_1]);
                    int b1 = numberOfBigram(textBigrams[b_1]);
                    int a2 = numberOfBigram(langBigrams[a_2]);
                    int b2 = numberOfBigram(textBigrams[b_2]);

                    std::vector<int> A = solve_lin_eq(a1 - a2, b1 - b2, M);
                    for (int a : A) {
                        int b = (b1 - a * a1) % M;
                        keys.push_back({ a, b });
                    }
                }
            }
        }
    }
    return keys;
}

std::string findBigram(int number) {
    int first_index = number / m;
    int second_index = number % m;
    std::string bigram = "";
    bigram += alphabet[first_index];
    bigram += alphabet[second_index];
    return bigram;
}

std::string dec_bigram(const std::string& txt, int a_inv, int b) {
    int Y = numberOfBigram(txt);
    if (Y == -1) {
        return "";
    }
    return findBigram(a_inv * (Y - b) % M);
}

std::string dec_text(const std::string& txt, const std::pair<int, int>& key) {
    int a = key.first;
    int b = key.second;
    std::vector<int> result = findGCD(a, M);
    int d = result[0];
    int a_inv = result[1];
    if (d != 1) {
        return "";
    }
    std::string res = "";
    for (int i = 1; i < txt.length(); i += 2) {
        std::string temp = "";
        temp += txt[i - 1];
        temp += txt[i];
        res += dec_bigram(temp, a_inv, b);
    }
    return res;
}

double calc_index(const std::string& txt) {
    double k = 0.0;
    int n = txt.length();
    for (char t : alphabet) {
        int tmp = 0;
        for (char i : txt) {
            if (i == t) {
                tmp += 1;
            }
        }
        k += (tmp * (tmp - 1));
    }
    k = k / (n * (n - 1));
    return k;
}

int main() {
    std::string text;
    std::ifstream file("./06.txt");
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            text += line;
        }
        file.close();
    }
    else {
        std::cout << "Unable to open the file" << std::endl;
        return 0;
    }

    text.erase(std::remove(text.begin(), text.end(), '\n'), text.end());

    std::vector<std::pair<int, int>> keys = findPair(textBigrams);
    for (const auto& key : keys) {
        std::string decoded_text = dec_text(text, key);
        if (decoded_text.empty()) {
            continue;
        }
        double diff = std::abs(calc_index(decoded_text) - I);
        if (diff < 0.001) {
            std::cout << decoded_text << std::endl;
            std::cout << key.first << ", " << key.second << std::endl;
            break;
        }
    }

    return 0;
}
