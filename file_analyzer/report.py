import json
from typing import Any

from .decorators import execution_stats, log_buffer, log_calls, measure_time 
from .scanner import scanner
from .utils import statistic_by_extensions


@measure_time("<REPORT_TIME>")
@log_calls
def default_output(extensions_stats_dict: dict, top_files: dict, top_count: int, path: str) -> tuple[str, str]:
    '''
    Write statistics in file or console

    '''

    files_stat_text = (
        f"Analysis path: {path}\n"
        f"Total files: {sum([x['count'] for x in extensions_stats_dict.values()])}\n"
        f"Total size: {sum([x['size'] for x in extensions_stats_dict.values()])} bytes\n\n\n"
    )
    
    extensions_stat_text = "By extension:\n"
    extensions_stats_list = []
    for key, value in extensions_stats_dict.items():
        extensions_stats_list.append((f"{repr(key)} - {value["count"]} files, {value["size"]} bytes\n"))
    extensions_stat_text += "".join(extensions_stats_list)

    extensions_stat_text += f"\n\nTop {top_count} largest files:\n"
    top_files_stat_list = []
    for idx, top_file in enumerate(top_files, 1):
        top_files_stat_list.append((f"{idx}. {repr(top_file["path"])} - {top_file["size"]} bytes\n"))
    extensions_stat_text += "".join(top_files_stat_list)

    return files_stat_text, extensions_stat_text


@measure_time("<REPORT_TIME>")
@log_calls
def json_output(extensions_stats_dict: dict, top_files: dict, path: str) -> dict[str, Any]:
    '''
    Write statistics in "report.json" file

    '''
    json_output_data = {
        "analysis_path": repr(path),
        "total_files": sum([x['count'] for x in extensions_stats_dict.values()]),
        "total_size": sum([x['size'] for x in extensions_stats_dict.values()]),
        "execution_info": {
                "scan_time": round(execution_stats["<SCAN_TIME>"], 2),
                "report_generation_time": 0
                },
        "by_extension": {key: value for key, value in extensions_stats_dict.items() if key},
        "<no extension>": extensions_stats_dict.get("", {"count": 0, "size": 0}),
        "top_files": top_files
    }

    return json_output_data
    

@measure_time("<REPORT_TIME>")
@log_calls
def report(args) -> tuple[Any, str]:
    all_filtered_paths_list = scanner(args)

    top_filtered_paths_list = sorted(all_filtered_paths_list, key=lambda x: x["size"], reverse=True)[:args.top]
    
    extensions_stats_dict = statistic_by_extensions(all_filtered_paths_list)
    
    if args.json:
        json_output_data = json_output(extensions_stats_dict, top_filtered_paths_list, args.path)
        json_output_data["execution_info"]["scan_time"] = round(execution_stats["<SCAN_TIME>"], 2)
        return (json_output_data, "")
    else:
        files_stat_text, extensions_stat_text = default_output(extensions_stats_dict, top_filtered_paths_list, args.top, args.path)
        return (files_stat_text, extensions_stat_text)


@log_calls
def report_output(args) -> None:
    output_data, second_part_output = report(args)

    if args.json:
        output_data["execution_info"]["report_generation_time"] = round(execution_stats["<REPORT_TIME>"], 2)
        try:
            with open("report.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Failed to write to {args.output}: {e}")
            raise
    else:
        time_stat_text = (
            f"Execution info:\n"
            f"scan time: {round(execution_stats["<SCAN_TIME>"], 2)} ms\n"
            f"Report generation time: {round(execution_stats["<REPORT_TIME>"], 2)} ms\n\n\n"
        )
        result_output_data = output_data + time_stat_text + second_part_output

        if args.output:
            try:
                with open(args.output, "w") as f:
                    f.write(result_output_data)
            except PermissionError as e:
                print(f"Critical output file access error {args.output}: {e}")
            except OSError as e:
                print(f"Failed to write to {args.output}: {e}")
        else:
            print(result_output_data)


def output_logs(is_file_output=True, output_file="log.txt"):
    if log_buffer:
        output = "\n".join(log_buffer)
        if is_file_output:
            try:
                with open(output_file, "w") as f:
                    f.write(output)
            except PermissionError as e:
                print(f"Critical output file access error {output_file}: {e}")
            except OSError as e:
                print(f"Failed to write to {output_file}: {e}")
        else:
            print(output)
