#ifndef PDBS_PATTERN_GENERATION_SINGLE_GREEDY_H
#define PDBS_PATTERN_GENERATION_SINGLE_GREEDY_H

#include "pattern_generator.h"

class Options;

class PatternGeneratorGreedy : public PatternGenerator {
    int max_states;
public:
    explicit PatternGeneratorGreedy(const Options &opts);
    explicit PatternGeneratorGreedy(int max_states);
    virtual ~PatternGeneratorGreedy() = default;

    virtual Pattern generate(std::shared_ptr<AbstractTask> task) override;
};

#endif
