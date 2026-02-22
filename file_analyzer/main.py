import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("PATH")
    # parser.add_argument("-h", "--help")
    parser.add_argument("--ext")
    parser.add_argument("--min-size")
    parser.add_argument("--max-size")
    parser.add_argument("--name")
    parser.add_argument("--top")
    parser.add_argument("--output")
    parser.add_argument("--json")
    args = parser.parse_args()
    print(args.PATH, args.top)
if __name__ == "__main__":
    main()