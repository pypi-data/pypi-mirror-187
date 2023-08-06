import argparse
from typing import Dict, List, Tuple

from .exeptions import ValidationError

slicing_abbr = slice(0, 3)
slicing_time = slice(14, 26)


def argument_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Report of Monaco racing")
    parser.add_argument(
        "--folder", type=str, help="path to folders with logs", required=True
    )
    parser.add_argument("--asc", help="ascending order of pilots", action="store_true")
    parser.add_argument(
        "--desc", help="descending order of pilots", action="store_true"
    )
    parser.add_argument("--driver", type=str, help="shows statistic about driver")
    return parser.parse_args()


def file_conversion(file_from_path: str) -> List[str]:
    try:
        with open(file_from_path, encoding="utf-8") as file_to_read:
            return file_to_read.readlines()
    except FileNotFoundError:
        raise ValidationError("This file not found, try another one!")


def log_conversion(list_of_log_lines: List[str]) -> Dict[str, str]:
    if not isinstance(list_of_log_lines, list):
        raise ValidationError("Here must be a list with strings from logfile")
    return {item_of_log[slicing_abbr]: item_of_log[slicing_time] for item_of_log in list_of_log_lines}


def abbr_conversion(list_of_abbr_lines: List[str]) -> Dict[str, Tuple[str, str]]:
    if not isinstance(list_of_abbr_lines, list):
        raise ValidationError(
            "Here must be a list with strings from abbreviations file"
        )
    split_abbreviation = [
        item_of_abbr.split("_") for item_of_abbr in list_of_abbr_lines
    ]
    return {
        abbreviation: (driver_name, team_name[:-1])
        for abbreviation, driver_name, team_name in split_abbreviation
    }
