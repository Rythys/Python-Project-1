import json
from decorators import log_calls, measure_time
from scanner import scanner
from utils import statistic_by_extensions


def default_output(is_file: bool, extensions_stats_dict: dict, top_files: dict, top_count: int, path: str):
    '''
    Write statistics in file or console

    '''
    stat_text = (
        f"Analysis path: {path}\n"
        f"Total files: {sum([x['count'] for x in extensions_stats_dict.values()])}\n"
        f"Total size: {sum([x['size'] for x in extensions_stats_dict.values()])} bytes\n\n\n"
        f"Execution info:\n"
        f"scan time: <SCAN TIME> ms\n"
        f"Report generation time: <REPORT TIME> ms\n\n\n"
        f"By extension:\n"
    )

    extensions_stats_list = []
    for key, value in extensions_stats_dict.items():
        extensions_stats_list.append((f"{repr(key)} - {value["count"]} files, {value["size"]} bytes\n"))
    stat_text += "".join(extensions_stats_list)

    stat_text += f"\n\nTop {top_count} largest files:\n"
    top_files_stat_list = []
    for idx, top_file in enumerate(top_files):
        top_files_stat_list.append((f"{idx}. {repr(top_file["path"])} - {top_file["size"]} bytes\n"))
    stat_text += "".join(top_files_stat_list)

    if is_file:
        with open(is_file, "w") as f:
            f.write(stat_text)
    else:
        print(stat_text)


def json_output(extensions_stats_dict: dict, top_files: dict, top_count: int, path: str):
    '''
    Write statistics in "report.json" file

    '''
    json_output_data = {
        "analysis_path": repr(path),
        "total_files": sum([x['count'] for x in extensions_stats_dict.values()]),
        "total_size": sum([x['size'] for x in extensions_stats_dict.values()]),
        "execution_info": {
                "scan_time": 150,
                "report_generation_time": 50
                },
        "by_extension": extensions_stats_dict,
        "top_files": top_files
    }   
    with open("report.json", 'w', encoding='utf-8') as f:
        json.dump(json_output_data, f, indent=2)


@measure_time
@log_calls
def report(args):
    all_filtered_paths_list = list(scanner(args))

    top_filtered_paths_list = sorted(all_filtered_paths_list, key=lambda x: x["size"], reverse=True)[:args.top]
    
    extensions_stats_dict = statistic_by_extensions(all_filtered_paths_list)
    
    if args.json:
        json_output(extensions_stats_dict, top_filtered_paths_list, args.top, args.path)
    else:
        default_output(args.output, extensions_stats_dict, top_filtered_paths_list, args.top, args.path)
