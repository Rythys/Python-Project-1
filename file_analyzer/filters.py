

def is_file_filtered_by_args(file, args):
    if args.ext and file.suffix != args.ext:
        return False

    if args.min_size and file.stat().st_size < args.min_size:
        return False

    if args.max_size and file.stat().st_size > args.max_size:
        return False

    if args.name and args.name not in file:
        return False
    return True


