from __future__ import annotations

import sys

from termcolor import colored

from jvnpack.harmonic_mean import harmonic_mean


def main():
    nums = _parse_nums(sys.argv[1:])
    mean = _calculate_results(nums)
    output = _format_output(mean)
    print(output)


def _parse_nums(inputs: list[str]) -> list[float]:
    try:
        nums = [float(i.strip()) for i in inputs]
    except ValueError:
        nums = []
    return nums


def _calculate_results(nums: list[float]) -> float:
    try:
        mean = harmonic_mean(nums)
    except ZeroDivisionError:
        mean = 0.0
    return mean


def _format_output(result: float) -> str:
    formated_result = colored(str(result), "red", "on_cyan", attrs=["bold"])
    return formated_result
