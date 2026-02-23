import json
from scanner import scanner
from utils import statistic_by_extensions


def default_output(file, extensions_stats_dict, top_files, top_count, path):
        stat_text = (
            f"Analysis path: {path}\n"
            f"Total files: {sum([x['count'] for x in extensions_stats_dict.values()])}\n"
            f"Total size: {sum([x['size'] for x in extensions_stats_dict.values()])} bytes\n\n\n"
            f"Execution info:\n"
            f"scan time: <SCAN TIME> ms\n"
            f"Report generation time: <REPORT TIME> ms\n\n\n"
            f"By extension:\n"
        )

        for key, value in extensions_stats_dict.items():
            stat_text += (f"{repr(key)} - {value["count"]} files, {value["size"]} bytes\n")

        stat_text += f"\n\nTop {top_count} largest files:\n"
        for idx, top_file in enumerate(top_files):
            stat_text += (f"{idx}. {repr(top_file["path"])} - {top_file["size"]} bytes\n")

        if file:
            with open(file, "w") as f:
                f.write(stat_text)
        else:
            print(stat_text)


def json_output(extensions_stats_dict, top_files, top_count, path):
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


def report(args):
    all_filtered_paths_list = list(scanner(args))

    top_filtered_paths_list = sorted(all_filtered_paths_list, key=lambda x: x["size"], reverse=True)[:args.top]
    
    extensions_stats_dict = statistic_by_extensions(all_filtered_paths_list)
    
    if args.json:
        json_output(extensions_stats_dict, top_filtered_paths_list, args.top, args.path)
    else:
        default_output(args.output, extensions_stats_dict, top_filtered_paths_list, args.top, args.path)
