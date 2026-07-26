#! /usr/bin/env python3

import platform
import re
import sys

from pathlib import Path

import pypddl_datasets

from downward.reports.absolute import AbsoluteReport
from lab.environments import TetralithEnvironment, LocalEnvironment
from lab.experiment import Experiment
from lab.reports import Attribute, geometric_mean
from search_parser import SearchParser

DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))

# Create custom report class with suitable info and error attributes.
class BaseReport(AbsoluteReport):
    INFO_ATTRIBUTES = ["wall_time_limit", "memory_limit"]
    ERROR_ATTRIBUTES = [
        "domain",
        "problem",
        "algorithm",
        "unexplained_errors",
        "error",
        "node",
    ]

DIR = Path(__file__).resolve().parent
REPO = DIR.parent

NODE = platform.node()
REMOTE = re.match(r"tetralith\d+.nsc.liu.se|n\d+", NODE)

if REMOTE:
    ENV = TetralithEnvironment(
        setup=TetralithEnvironment.DEFAULT_SETUP,
        memory_per_cpu="2840M",
        cpus_per_task=6,  # 6*2840 >= 16000
        extra_options="#SBATCH --account=naiss2025-5-382")
    
else:
    ENV = LocalEnvironment(processes=6)

if REMOTE:
    SUITES = [
        "autoscale-agile-strips",
        "htg",
    ]
    WALL_TIME_LIMIT = 10 * 60
else:
    SUITES = [
        "ipc-satisficing-strips-test",
        "ipc-satisficing-adl-test",
        "autoscale-agile-strips-test",
    ]
    WALL_TIME_LIMIT = 5

ATTRIBUTES = [
    "run_dir",
    "coverage",
    "unsolvable",
    "initial_h_value",
    "search_time_s",
    "total_time_s",
    "num_generated",
    "num_expanded",
    "search_time_ms_per_expanded",
    "cost",
    "length",
    "invalid",
    "memory_mb",
]


MEMORY_LIMIT = 16000

# Create a new experiment.
exp = Experiment(environment=ENV)
# Add custom parser for FF.
exp.add_parser(SearchParser())


exp.add_resource("fast_downward_py", str(REPO / "fast-downward.py"))
exp.add_resource("driver", str(REPO / "driver"))
exp.add_resource("translator", str(REPO / "builds" / "release" / "bin" / "translate"), str(Path("builds") / "release" / "bin" / "translate"))
exp.add_resource("downward", str(REPO / "builds" / "release" / "bin" / "downward"), str(Path("builds") / "release" / "bin" / "downward"))
exp.add_resource("planner_exe", DIR / "gbfs-lazy-hff-pref-ff.sh")

for SUITE in SUITES:
    for domain in pypddl_datasets.fetch_suite(SUITE).domains:
        for task in domain.tasks:
            run = exp.add_run()
            run.add_resource("domain", task.domain_path, symlink=True)
            run.add_resource("problem", task.task_path, symlink=True)
            run.add_command(
                "run_planner",
                ["{planner_exe}", "{fast_downward_py}", "{domain}", "{problem}", "sas_plan"],
                wall_time_limit=WALL_TIME_LIMIT,
                memory_limit=MEMORY_LIMIT,
            )
            run.set_property("domain", task.domain)
            run.set_property("problem", task.problem)
            run.set_property("algorithm", "downward-gbfs-lazy-hff-pref-ff")
            run.set_property("wall_time_limit", WALL_TIME_LIMIT)
            run.set_property("memory_limit", MEMORY_LIMIT)
            run.set_property("id", ["downward-gbfs-lazy-hff-pref-ff", task.domain, task.problem])

# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

exp.add_step("parse", exp.parse)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

# Make a report.
exp.add_report(BaseReport(attributes=ATTRIBUTES), outfile="report.html")

# Parse the commandline and run the specified steps.
exp.run_steps()
