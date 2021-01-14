import ClassParser

def ExFunc(class_) -> str:

    generatedfunc = "\n"
    class_.generated = "\npublic:void print();\n"
    for var_ in class_.variables:
        if "print" in var_.tags:
            generatedfunc += f"\tstd::cout << \"{var_.variablename}\" << {var_.variablename} << \'\\n\';\n"
    return f"\nvoid {class_.typename}::print()\n" + "{" + generatedfunc + "}"


ClassParser.ParseClass("example/example.h","example/example.cpp",ExFunc)