#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from scratch_project.crew import ScratchProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    inputs = {
        'ticker': 'NVDA',
    }

    ScratchProject().crew().kickoff(inputs=inputs)


def train():
    inputs = {
        'ticker': 'NVDA'
    }
    ScratchProject().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)


def replay():
    ScratchProject().crew().replay(task_id=sys.argv[1])

def test():
    inputs = {
        "ticker": "NVDA",
    }

    ScratchProject().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

