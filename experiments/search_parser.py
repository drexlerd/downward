#! /usr/bin/env python

from lab.parser import Parser


def process_unsolvable(content, props):
    props["unsolvable"] = int("exhausted" in props)

def process_invalid(content, props):
    props["invalid"] = int("invalid" in props)

def process_memory(content, props):
    if "memory" in props:
        props["memory"] = props["memory"] / 1000

def add_coverage(content, props):
    if "cost" in props or props.get("unsolvable", 0):
        props["coverage"] = 1
    else:
        props["coverage"] = 0

def add_search_time_us_per_expanded(context, props):
    if "search_time" in props:
        if props["num_expanded"] == 0:
            props["search_time_us_per_expanded"] = 1
        else:
            props["search_time_us_per_expanded"] = (props["search_time"] * 1_000_000) / props["num_expanded"]
 
def compute_total_time(content, props):
    # total_time is translation_time + search_time
    if "translation_time" in props and "search_time" in props:
        props["total_time"] = props["translation_time"] + props["search_time"]

class SearchParser(Parser):
    """
    Reordering and filtering variables: [0.000s CPU, 0.000s wall-clock]
    Translator variables: 5
    Translator derived variables: 0
    Translator facts: 14
    Translator goal facts: 1
    Translator mutex groups: 2
    Translator total mutex groups size: 6
    Translator operators: 18
    Translator axioms: 0
    Translator task size: 120
    Translator peak memory: 53152 KB
    Writing output... [0.000s CPU, 0.000s wall-clock]
    Done! [0.000s CPU, 0.003s wall-clock]
    translate exit code: 0

    INFO     Running search (release).
    INFO     search stdin: output.sas
    INFO     search time limit: None
    INFO     search memory limit: None
    INFO     search command line string: /home/dominik/projects/code/downward/builds/release/bin/downward --search 'lazy_greedy([ff()], preferred=[ff()], boost=1000, randomize_successors=true, random_seed=0)' --internal-plan-file sas_plan < output.sas
    [t=0.000076s, 10864 KB] Search code revision: aaeb23f36
    [t=0.000136s, 10864 KB] reading input...
    [t=0.000230s, 10864 KB] done reading input!
    [t=0.000865s, 11120 KB] Simplifying 34 unary operators... done! [34 unary operators]
    [t=0.000898s, 11120 KB] time to simplify: 0.000040s
    [t=0.000909s, 11120 KB] Initializing additive heuristic...
    [t=0.000917s, 11120 KB] Initializing FF heuristic...
    [t=0.000933s, 11120 KB] Simplifying 34 unary operators... done! [34 unary operators]
    [t=0.000949s, 11120 KB] time to simplify: 0.000022s
    [t=0.000957s, 11120 KB] Initializing additive heuristic...
    [t=0.000964s, 11120 KB] Initializing FF heuristic...
    [t=0.000981s, 11120 KB] Building successor generator... done!
    [t=0.001007s, 11120 KB] peak memory difference for successor generator creation: 0 KB
    [t=0.001013s, 11120 KB] time for successor generation creation: 0.000009s
    [t=0.001020s, 11120 KB] Variables: 5
    [t=0.001026s, 11120 KB] FactPairs: 14
    [t=0.001032s, 11120 KB] Bytes per state: 4
    [t=0.001046s, 11120 KB] Conducting lazy best first search, (real) bound = 2147483647
    [t=0.001061s, 11120 KB] New best heuristic value for ff: 3
    [t=0.001068s, 11120 KB] g=0, 1 evaluated, 0 expanded
    [t=0.001080s, 11256 KB] Initial heuristic value for ff: 3
    [t=0.001091s, 11256 KB] Initial heuristic value for ff: 3
    [t=0.001103s, 11256 KB] New best heuristic value for ff: 2
    [t=0.001109s, 11256 KB] g=1, 3 evaluated, 2 expanded
    [t=0.001118s, 11256 KB] New best heuristic value for ff: 1
    [t=0.001124s, 11256 KB] g=2, 4 evaluated, 3 expanded
    [t=0.001132s, 11256 KB] Solution found!
    [t=0.001138s, 11256 KB] Actual search time: 0.000089s
    pick ball2 rooma left (1)
    move rooma roomb (1)
    drop ball2 roomb left (1)
    [t=0.001145s, 11256 KB] Plan length: 3 step(s).
    [t=0.001145s, 11256 KB] Plan cost: 3
    [t=0.001145s, 11256 KB] Expanded 4 state(s).
    [t=0.001145s, 11256 KB] Reopened 0 state(s).
    [t=0.001145s, 11256 KB] Evaluated 5 state(s).
    [t=0.001145s, 11256 KB] Evaluations: 9
    [t=0.001145s, 11256 KB] Generated 13 state(s).
    [t=0.001145s, 11256 KB] Dead ends: 0 state(s).
    [t=0.001145s, 11256 KB] Number of registered states: 5
    [t=0.001145s, 11256 KB] Int hash set load factor: 5/8 = 0.625000
    [t=0.001145s, 11256 KB] Int hash set resizes: 3
    [t=0.001145s, 11256 KB] Search time: 0.000099s
    [t=0.001145s, 11256 KB] Total time: 0.001145s
    Solution found.
    Peak memory: 11256 KB
    Remove intermediate file output.sas
    search exit code: 0

    INFO     Planner time: 0.06s
    """
    def __init__(self):
        super().__init__()
        self.add_pattern("translation_time", r"Done! \[.*s CPU, (.*)s wall-clock\]", type=float)
        self.add_pattern("search_time", r"Search time: (.+)s", type=float)  
        self.add_pattern("total_time", r"Planner time: (.*)s", type=float)
        self.add_pattern("num_expanded", r"Expanded (\d+) state\(s\).", type=int)
        self.add_pattern("num_generated", r"Generated (\d+) state\(s\).", type=int)
        self.add_pattern("cost", r"Plan cost: (\d+)", type=int)
        self.add_pattern("length", r"Plan length: (\d+) step\(s\).", type=int)
        self.add_pattern("initial_h_value", r"Initial heuristic value for ff: (\d+)", type=int)
        self.add_pattern("invalid", r"(Plan invalid)", type=str)
        self.add_pattern("memory", r"Peak memory: (\d+) KB", type=int)

        self.add_function(process_unsolvable)
        self.add_function(process_invalid)
        self.add_function(process_memory)
        self.add_function(add_coverage)
        self.add_function(add_search_time_us_per_expanded)