#! /usr/bin/env python

#from lab.environments import LocalEnvironment
from lab.environments import FreiburgSlurmEnvironment

import os.path
import os

from downward.experiment import FastDownwardExperiment
from downward.reports.absolute import AbsoluteReport
from downward.reports.scatter import ScatterPlotReport


# my version of fast downward
REPO = os.path.expanduser('~/downward')
# the set of benchmarks to evaluate on
BENCHMARKS = os.path.expanduser('~/benchmarks/downward-benchmarks')
## ALL
SUITE = ["assembly", "miconic-fulladl", "openstacks", "openstacks-opt08-adl", "optical-telegraphs", "philosophers", "psr-large", "psr-middle", "trucks"]

REVISION_CACHE = os.path.expanduser('~/fd-lab-freiburg/experiments/cpu-benchmarks/data/revision-cache')

# Note: if we use 4G=4096M>4000M then 2 cores are being occupied.
ENV = FreiburgSlurmEnvironment()

# Setup the experiments
exp = FastDownwardExperiment(environment=ENV, revision_cache=REVISION_CACHE)

exp.add_suite(BENCHMARKS, SUITE)

exp.add_algorithm("issue348-base", REPO, "issue348-base", ["--search", "astar(blind())"])
exp.add_algorithm("issue348-v20", REPO, "issue348-v20", ["--search", "astar(blind())"])

# "For single-search experiments, we recommend adding the following parsers in this order:"
exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

# the steps to be executed
exp.add_step('build', exp.build)
exp.add_step('start', exp.start_runs)
exp.add_parse_again_step()
exp.add_fetcher(name='fetch')
exp.add_report(AbsoluteReport(), outfile='report.html')

exp.run_steps()
