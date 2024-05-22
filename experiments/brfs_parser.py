#! /usr/bin/env python

from lab.parser import Parser

def search_time_to_ms(content, props):
    if "search_time" in props:
        props["search_time"] = props["search_time"] * 1000

def coverage(content, props):
    props["coverage"] = int("cost" in props)

def unsolvable(content, props):
    props["unsolvable"] = int("exhausted" in props)

def invalid_plan_reported(content, props):
    props["invalid_plan_reported"] = int("val_plan_invalid" in props)

class BrfsParser(Parser):
    """
    Successful Run:
    [t=0.004009s, 10816 KB] Plan cost: 11
    [t=0.004009s, 10816 KB] Search time: 0.000000s
    [t=0.004009s, 10816 KB] Total time: 0.004009s
    [t=0.004009s, 10816 KB] Expanded 239 state(s).
    [t=0.004009s, 10816 KB] Generated 832 state(s).
    [t=0.004009s, 10816 KB] Expanded until last jump: 234 state(s).
    [t=0.004009s, 10816 KB] Generated until last jump: 818 state(s).

    Unsolvable Run:
    Search stopped without finding a solution.

    Validate output:
    Plan executed successfully - checking goal
    Plan valid
    Final value: 11

    Plan executed successfully - checking goal
    Goal not satisfied
    Plan invalid
    """
    def __init__(self):
        super().__init__()
        self.add_pattern("search_time", r"\[.*\] Search time: (.+)s", type=float)
        self.add_pattern("num_expanded", r"\[.*\] Expanded (\d+) state\(s\).", type=int)
        self.add_pattern("num_generated", r"\[.*\] Generated (\d+) state\(s\).", type=int)
        self.add_pattern("num_expanded_until_last_f_layer", r"\[.*\] Expanded until last jump: (\d+) state\(s\).", type=int)
        self.add_pattern("num_generated_until_last_f_layer", r"\[.*\] Generated until last jump: (\d+) state\(s\).", type=int)
        self.add_pattern("cost", r"\[.*\] Plan cost: (.+)", type=float)
        self.add_pattern("exhausted", r"(Search stopped without finding a solution.)", type=str)
        self.add_pattern("val_plan_invalid", r"(Plan invalid)", type=str)

        self.add_function(coverage)
        self.add_function(unsolvable)
        self.add_function(invalid_plan_reported)
        self.add_function(search_time_to_ms)
