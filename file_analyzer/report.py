import json
from decorators import log_calls, measure_time
from scanner import scanner
from utils import statistic_by_extensions


@measure_time
@log_calls
def default_output(extensions_stats_dict: dict, top_files: dict, top_count: int, path: str):
    '''
    Write statistics in file or console

    '''
    files_stat_text = (
        f"Analysis path: {path}\n"
        f"Total files: {sum([x['count'] for x in extensions_stats_dict.values()])}\n"
        f"Total size: {sum([x['size'] for x in extensions_stats_dict.values()])} bytes\n\n\n"
    )
    
    extensions_stat_text = f"By extension:\n"
    extensions_stats_list = []
    for key, value in extensions_stats_dict.items():
        extensions_stats_list.append((f"{repr(key)} - {value["count"]} files, {value["size"]} bytes\n"))
    extensions_stat_text += "".join(extensions_stats_list)

    extensions_stat_text += f"\n\nTop {top_count} largest files:\n"
    top_files_stat_list = []
    for idx, top_file in enumerate(top_files):
        top_files_stat_list.append((f"{idx}. {repr(top_file["path"])} - {top_file["size"]} bytes\n"))
    extensions_stat_text += "".join(top_files_stat_list)

    return files_stat_text, extensions_stat_text


@measure_time
@log_calls
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
        "by_extension": {key: value for key, value in extensions_stats_dict.items() if key},
        "<no extension>": extensions_stats_dict.get("", {"count": 0, "size": 0}),
        "top_files": top_files
    }

    return json_output_data
    


@measure_time
@log_calls
def report(args):
    all_filtered_paths_list, scanner_work_time = scanner(args)

    top_filtered_paths_list = sorted(all_filtered_paths_list, key=lambda x: x["size"], reverse=True)[:args.top]
    
    extensions_stats_dict = statistic_by_extensions(all_filtered_paths_list)
    
    if args.json:
        json_output_data, json_output_work_time = json_output(extensions_stats_dict, top_filtered_paths_list, args.top, args.path)
        json_output_data["execution_info"]["scan_time"] = scanner_work_time
        json_output_data["execution_info"]["report_generation_time"] = json_output_work_time
        try:
            with open("report.json", 'w', encoding='utf-8') as f:
                json.dump(json_output_data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Failed to write to 'report.json': {e}")
            raise
    else:
        partition_of_stat_text, default_output_work_time = default_output(extensions_stats_dict, top_filtered_paths_list, args.top, args.path)
        files_stat_text, extensions_stat_text = partition_of_stat_text
        time_stat_text = (
            f"Execution info:\n"
            f"scan time: {scanner_work_time} ms\n"
            f"Report generation time: {default_output_work_time} ms\n\n\n"
        )
        result_output_data = files_stat_text + time_stat_text + extensions_stat_text

        if args.output:
            try:
                with open(args.output, "w") as f:
                    f.write(result_output_data)
            except OSError as e:
                print(f"Failed to write to {args.output}: {e}")
                raise
        else:
            print(result_output_data)