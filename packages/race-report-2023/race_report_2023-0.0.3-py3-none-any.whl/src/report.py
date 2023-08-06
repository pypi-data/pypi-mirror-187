import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from .constants import ABBR_FILE, START_LOG, STOP_LOG, TIME_FORMAT
from .exeptions import ValidationError
from .file_process import abbr_conversion, file_conversion, log_conversion

slicing_time_m_s_ss = slice(2, -3)


@dataclass
class Driver:
    name: str
    team: str
    time: str
    abbr: str

    def __repr__(self):
        return (f"\nDriver name :     {self.name!r}\n"
                f"Team name:        {self.team!r}\n"
                f"Lap time:         {self.time!r}\n"
                f"Abbreviation:     {self.abbr!r}\n")


def build_report(path_to_file: str) -> List[Driver]:
    if not isinstance(path_to_file, str):
        raise ValidationError("Here must be a path to file folder")

    start_log = os.path.join(path_to_file, START_LOG)
    end_log = os.path.join(path_to_file, STOP_LOG)
    abbr_log = os.path.join(path_to_file, ABBR_FILE)

    start_log_data = log_conversion(file_conversion(start_log))
    end_log_data = log_conversion(file_conversion(end_log))
    abbr_data = abbr_conversion(file_conversion(abbr_log))

    time_lap = get_time_lap(start_log_data, end_log_data)

    printing_list = [
        Driver(name=abbr_data[key][0], team=abbr_data[key][1], time=time_lap[key], abbr=key) for key in abbr_data
    ]
    return printing_list


def get_time_lap(start_log_data: Dict[str, str], end_log_data: Dict[str, str]) -> Dict[str, str]:
    lap_time = {}
    for key in start_log_data:
        if end_log_data[key] > start_log_data[key]:
            lap_time[key] = str(
                datetime.strptime(end_log_data[key], TIME_FORMAT)
                - datetime.strptime(start_log_data[key], TIME_FORMAT)
            )[slicing_time_m_s_ss]
        else:
            lap_time[key] = "Fail_Time"
    return lap_time


def print_report(list_of_results: List[Driver]) -> None:
    if not isinstance(list_of_results, list):
        raise ValidationError("Somthing wrong with data, in function build_report")
    final_print, final_negative_timers_print = [], []
    for item in list_of_results:
        if item.time != "Fail_Time":
            final_print.append(item)
        else:
            final_negative_timers_print.append(item)

    data_alignment(final_print)
    print("  -----=====  Racers with bad time in logs   =====-----")
    data_alignment(final_negative_timers_print)


def finding_driver(list_of_results: List[Driver], driver_name: str) -> List[Driver]:
    driver = [item for item in list_of_results if item.name.lower() == driver_name.lower()]
    return driver


def print_driver_stat(list_of_results: List[Driver], driver_name: str) -> None:
    if not isinstance(list_of_results, list):
        raise ValidationError("Somthing wrong with data, in function build_report")
    print(finding_driver(list_of_results, driver_name)[0])


def list_sorting(time_lap_list: List[Driver], order: bool) -> List[Driver]:
    if not isinstance(time_lap_list, list):
        raise ValidationError("Incoming data is not a list")
    time_lap_list.sort(key=lambda driver: driver.time, reverse=order)
    return time_lap_list


def data_alignment(list_of_data: List[Driver]) -> None:
    if not isinstance(list_of_data, list):
        raise ValidationError("Somthing wrong with data, in function build_report")
    for result_counter in range(len(list_of_data)):
        if result_counter == 15:
            print("|", "-" * 66, "|")
        print_leveler = 0 if result_counter < 9 else ''
        print(
            f"|{print_leveler}{result_counter + 1} | {list_of_data[result_counter].name}".ljust(25),
            f"| {list_of_data[result_counter].team}".ljust(30),
            f"| {list_of_data[result_counter].time} |",
        )
