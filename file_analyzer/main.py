import argparse
from report import report

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

    if args.min_size < 0:
        parser.error(f"Minimum size cannot be negative (got: {args.min_size})")
    if args.max_size and args.max_size < 0:
        parser.error(f"Maximim size cannot be negative (got: {args.max_size})")
    if args.top <= 0:
        parser.error(f"Minimum top files cannot be positive (got: {args.top})")

    report(args)

if __name__ == "__main__":
    main()
