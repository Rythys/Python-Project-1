<<<<<<< HEAD
<<<<<<< HEAD
import argparse
from report import report
=======
import argparse
from scanner import scanner
from utils import statistic_by_extensions

>>>>>>> 5603267e65736c5c6b51f094cb8ca4eed4b6f877

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("path", type=str)
    parser.add_argument("--ext", type=str, default=None)
    parser.add_argument("--min-size", type=int, default=0)
    parser.add_argument("--max-size", type=int, default=None)
    parser.add_argument("--name", type=str, default=None)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--json", type=bool, default=False)
    
    args = parser.parse_args()
<<<<<<< HEAD
    report(args)
    

if __name__ == "__main__":
    main()
=======
>>>>>>> main
=======
    all_filtered_paths_list = list(scanner(args))

    if args.top:
        top_filtered_paths_list = sorted(all_filtered_paths_list, \
                                         key=lambda x: x["size"], \
                                         reverse=True)[:args.top]
    # print(top_filtered_paths_list)

    extensions_stats_dict = statistic_by_extensions(all_filtered_paths_list)
    # print(extensions_stats_dict)
    
if __name__ == "__main__":
    main()
>>>>>>> 5603267e65736c5c6b51f094cb8ca4eed4b6f877
