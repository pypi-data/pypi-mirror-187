from src.file_process import argument_parser
from src.report import (build_report, list_sorting, print_driver_stat,
                        print_report)

if __name__ == "__main__":
    args = argument_parser()
    list_of_results = build_report(args.folder)

    if args.driver:
        print_driver_stat(list_of_results, args.driver)
    else:
        order = bool(args.desc)
        sorted_list_of_results = list_sorting(list_of_results, order)
        print_report(sorted_list_of_results)
