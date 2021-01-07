
# reneme this function
def findEnd(body: str, startIndex: int, openChar: str, closeChar: str) -> int:

    # Return if the starting character doesn't matches the charecter at the given index
    if(body[startIndex] != openChar):
        print("invalid openChar")
        return str()

    index = startIndex + 1

    counter: int = 1
    while(counter > 0):
        if(body[index] == openChar):
            counter += 1

        if(body[index] == closeChar):
            counter -= 1

        index += 1

    return index
    # return body[startIndex + 1:index - 1]


def TurnTotag(raw: str) -> str:
    return "/*[" + raw + "]*/"


class CPP_var:
    typename: str
    variablename: str
    tags = list()

    def __init__(self, data: str):
        data = data.strip()

        # Get the tags
        while(True):
            tagind = data.find("/*[")
            if(tagind != -1):
                tags = list()
                self.tags.append(data[tagind + len("/*["):data.find("]*/")])
                data = data[0:tagind] + \
                    data[data.find("]*/") + len("]*/"):len(data)]
            else:
                break

        esign = data.find("=")
        if(esign != -1):
            data = data[0:esign]

        data = data.strip()

        splitted = data.rsplit(" ", 1)

        if(len(splitted) != 2):
            print("invalid variable")
            print(splitted)
            return

        self.typename = splitted[0]
        self.variablename = splitted[1]


generatedField_TagS = TurnTotag("GeneratedField START")
generatedField_TagE = TurnTotag("GeneratedField END")


class CPP_class:
    typename: str
    variables: list
    raw: str
    generated: str

    def __init__(self, typename: str, data: str):
        self.typename = typename
        self.raw = data
        b: str = data.find(generatedField_TagS)

        # remove the generated code
        if(b != -1):
            data = data[0:b] + \
                data[data.find(generatedField_TagE) +
                     len(generatedField_TagE):len(data)]

        # remove comments
        while(True):
            comment = data.find("//")
            if(comment != -1):
                data = data[0:comment] + \
                    data[data.find("\n") + len("\n"):len(data)]
            else:
                break

        # remove comments while ignoreing tags
        while(True):
            comment = data.find("/*")
            if(comment != -1):
                if(data[comment + 2] != "["):
                    data = data[0:comment] + \
                        data[data.find("*/") + len("*/"):len(data)]
            else:
                break

        while(True):
            brac = data.find("{")
            if(brac != -1):
                data = data[0:brac] + \
                    data[findEnd(data, brac, "{", "}"):len(data)]
            else:
                break

        while(True):
            brac = data.find("(")
            if(brac != -1):
                data = data[0:brac] + \
                    data[findEnd(data, brac, "(", ")"):len(data)]
            else:
                break

        data.replace("\t", " ")
        data.replace("\n", " ")

        data.replace("struct", "")
        data.replace("class", "")

        splitmarker = "/*split!*/"

        data = data.replace(";", splitmarker)
        var = data.split(splitmarker)

        self.variables = list()
        for v in var:
            cppv = CPP_var(v)
            if(hasattr(cppv, "variablename")):
                self.variables.append(cppv)

class CPP_Parser