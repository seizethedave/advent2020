#include <fstream>
#include <iostream>
#include <string>

// To build:
// g++ 05a.cpp -std=c++11

const char* Filename = "advent05.txt";

int seatNumber(const std::string& row, const std::string& col) {
    uint8_t rowNum = 0;
    uint8_t pow = 1 << 6;

    for (char const &c: row) {
        if (c == 'B') {
            rowNum |= pow;
        }
        pow >>= 1;
    }

    uint8_t colNum = 0;
    pow = 1 << 2;

    for (char const &c: col) {
        if (c == 'R') {
            colNum |= pow;
        }
        pow >>= 1;
    }

    return int(rowNum) * 8 + int(colNum);
}

int main(int argc, char** argv) {
    std::ifstream input(Filename, std::ios::in);
    std::string line;
    int highest = 0;

    while (std::getline(input, line)) {
        std::string row(line, 0, 7);
        std::string col(line, 7, 3);
        int num = seatNumber(row, col);
        std::cout << num << std::endl;
        highest = std::max(highest, num);
    }

    std::cout << "highest = " << highest << std::endl;

    return 0;
}