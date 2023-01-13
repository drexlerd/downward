#ifndef UTILS_STRINGS_H
#define UTILS_STRINGS_H

#include "exceptions.h"

#include <sstream>
#include <string>

namespace utils {
class StringOperationError : public Exception {
public:
    using Exception::Exception;
};

extern void lstrip(std::string &s);
extern void rstrip(std::string &s);
extern void strip(std::string &s);

/*
  Split a given string at the first occurrence of separator or throw
  StringOperationError if separator is not found.
*/
extern std::pair<std::string, std::string> split(
    const std::string &s, const std::string &separator);

extern bool startswith(const std::string &s, const std::string &prefix);

template<typename Collection>
std::string join(const Collection &collection, const std::string &delimiter) {
    std::ostringstream oss;
    bool first_item = true;

    for (const auto &item : collection) {
        if (first_item)
            first_item = false;
        else
            oss << delimiter;
        oss << item;
    }
    return oss.str();
}
}
#endif
