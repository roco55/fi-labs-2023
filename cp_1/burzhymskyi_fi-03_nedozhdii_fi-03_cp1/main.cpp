#include <iostream>
#include <fstream>
#include <vector>
#include <cwctype>
#include <map>
#include <wchar.h>
#include <cmath>
#include <iomanip>

using namespace std;

wstring cleanText()
{
    std::wifstream inputFile("../text/text1.txt");

    std::locale loc("ru_RU.UTF-8");
    inputFile.imbue(loc);


    std::wcout.imbue(loc);
    std::wcout.setf(std::ios::boolalpha);

    std::wstring line;
    std::wstring text = L"";
    while (std::getline(inputFile, line))
    {
        for (auto c : line)
        {
            if (((c >= L'a' && c <= L'я') || c == L' ') && !(c>='a' && c<='z')
            && c!=L'©' && c!=L'«'&& c!= L'»' && c != L'á' && c != L'é' && c != L'ê' && c!=L'½')
            {
                text += static_cast<wchar_t >(std::towlower(c));
            }else if(c == L'-')
                text += L' ';
        }
        text += L' ';
    }
    inputFile.close();
    bool space = false;
    wstring formatted = L"";
    for(auto c : text)
    {
        if(c == L' ' && space == false)
        {
            space = true;
            formatted += ' ';
            continue;
        }

        if(c != L' ')
        {
            space = false;
            formatted += c;
        }
    }

    return formatted;
}

void H1(const wstring& text)
{
    map<wchar_t, int> gram;
    wcout<<'\n';
    for (auto c : text)
    {
        ++gram[c];
    }
    long long sum = 0;
    for (const auto& [key, value] : gram) {
        std::wcout << key << ": " << value << std::endl;
        sum+=value;
    }
    for (const auto& [key, value] : gram) {
        std::wcout <<"\'"<< key << "\'& " << (double)value/(double)sum<<" & " ;
    }
    wcout<<'\n';
    double h1 = 0;
    for (const auto& [key, value] : gram) {
        double p = (double)value/(double)sum;
        h1 += p*log2(p);
    }
    h1 = (-1)*h1;
    wcout<<"H1 = "<<h1;
    wcout<<'\n';
}


wstring clearSpaces(const wstring& text)
{
    wstring result = L"";
    for (auto c : text)
    {
        if(c != L' ')
            result += c;
    }

    return result;
}


void printBigramFreq(map<wstring, int> bigram)
{
    std::wcout<<bigram.size()-1<<'\n';
    long long sum = 0;
    for (const auto& [key, value] : bigram) {
        sum+=value;
    }

    for (const auto& [key, value] : bigram) {
        std::wcout <<"\'"<< key<<"\'" << ":" <<std::setprecision(7)<<std::fixed<< (double)value/(double)sum << "\n";
    }


    wcout<<'\n';
    double h2 = 0;
    for (const auto& [key, value] : bigram) {
        double p = (double)value/(double)sum;
        h2 += p*log2(p);
    }
    h2 = (-1)*h2;
    wcout<<"H2 = "<<h2/2<<'\n';
}

void H2(wstring text)
{
    map<wstring, int> bigram;
    wcout<<'\n';
    wcout<<L"Біграми з перетином літер з пробілом:\n";
    for(int i = 0; i < text.size() - 1; ++i)
    {
        wchar_t* a;
        wchar_t* b;
        if(text[i] == L' ')
            a = new wchar_t('_');
        else
            a = new wchar_t(text[i]);
        if(text[i+1] == L' ')
            b = new wchar_t ('_');
        else
            b = new wchar_t (text[i+1]);

        wstring tmp = static_cast<wstring>(a)+ static_cast<wstring>(b);
        bigram[tmp]++;
        delete a;
        delete b;
    }
    printBigramFreq(bigram);
    wcout<<'\n';


    bigram.clear();
    wcout<<L"Біграми без перетину літер з пробілами:\n";
    for(int i = 0; i < text.size() - 1; i+=2)
    {
        wchar_t* a;
        wchar_t* b;
        if(text[i] == L' ')
            a = new wchar_t('_');
        else
            a = new wchar_t(text[i]);
        if(text[i+1] == L' ')
            b = new wchar_t ('_');
        else
            b = new wchar_t (text[i+1]);
        wstring tmp = static_cast<wstring>(a) + static_cast<wstring>(b);
        bigram[tmp]++;
        delete a;
        delete b;
    }
    printBigramFreq(bigram);
    wcout<<'\n';


    text = clearSpaces(text);

    bigram.clear();
    wcout<<L"Біграми з перетином літер без пробілів:\n";
    for(int i = 0; i < text.size() - 1; ++i)
    {
        wchar_t* a = new wchar_t(text[i]);
        wchar_t* b = new wchar_t (text[i+1]);
        wstring tmp = static_cast<wstring>(a) + static_cast<wstring>(b);
        bigram[tmp]++;
        delete a;
        delete b;
    }
    printBigramFreq(bigram);
    wcout<<'\n';


    bigram.clear();
    wcout<<L"Біграми без перетину літер без пробілів:\n";
    for(int i = 0; i < text.size() - 1; i+=2)
    {
        wchar_t* a = new wchar_t(text[i]);
        wchar_t* b = new wchar_t (text[i+1]);
        wstring tmp = static_cast<wstring>(a) + static_cast<wstring>(b);
        bigram[tmp]++;
        delete a;
        delete b;
    }
    printBigramFreq(bigram);
    wcout<<'\n';





}





int main()
{
    setlocale(LC_ALL, "ru_RU.UTF-8");

    wstring cleaned = cleanText();
    //H1(cleaned);
    //H1(clearSpaces(cleaned));

    H2(cleaned);


    return 0;
}
