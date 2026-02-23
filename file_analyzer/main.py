<<<<<<< HEAD
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
    report(args)
    

if __name__ == "__main__":
    main()
=======
>>>>>>> main
