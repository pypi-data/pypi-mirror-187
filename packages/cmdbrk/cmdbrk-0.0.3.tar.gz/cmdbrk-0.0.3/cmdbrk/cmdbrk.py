from typing import List, Dict, TypedDict

HandledArguments = TypedDict("HandledArguments", {"other": Dict[int, str], "flags": List[str], "options": Dict[str, str]})

def handle(argv: List[str], prefix: str = "-") -> HandledArguments:
    """Handle arguments `argv`

       argv (List[str]): Arguments to handle.
    """
    index: int = 0

    other = {} 
    flags = []
    options = {}

    while index < len(argv):
        arg = argv[index]
        if arg.startswith(prefix):
            if flags.count(arg) > 0 or arg in options.keys():
                raise Exception(f"Cannot have duplicate flags/options ({arg})")

            if index < len(argv)-1:
                if argv[index+1].startswith(prefix):
                    flags.append(arg[len(prefix):])
                else:
                    options[arg[len(prefix):]] = argv[index+1]
                    index+=1
            else:
                flags.append(arg[len(prefix):])
        else:
            other[index] = arg
        index+=1;

    return {
        "other": other,
        "flags": flags,
        "options": options
    }


