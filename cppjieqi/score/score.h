#ifndef score_h
#define score_h

#include <unordered_map>
#include <algorithm>
#include <locale>
#include <sstream>
#include <fstream>
#include <locale>
#include <stdio.h>
#include "../log/log.h"
#include "../global/global.h"

#define RETURN memset(pst, 0, sizeof(pst)); return;
#define ENCODE(x, y) ((16 * (x)) + (y) + 51)

typedef unsigned short(*SCORE)(const char*, unsigned char, unsigned char);

unsigned short trivial_score_function(const char*, unsigned char, unsigned char);
void register_score_functions();
inline std::string trim(const std::string &s);
inline std::string sub(const std::string &s);
void read_score_table(const char* score_file);

#endif
