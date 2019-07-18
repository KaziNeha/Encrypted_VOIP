import os

GroupID = ["P2P", "224.1.1.1", "224.1.1.1",  "224.1.1.1", "224.1.1.1", "224.1.1.1"]
key = ["16digitNo", "16digitNo1234567", "16digitNo1234567", "16digitNo1234567", "16digitNo1234567", "16digitNo1234567"]

def JsonFormatToCopy():
    rs = ""

    rs += "{\\n"

    for i in range(0, len(GroupID)):
        rs += "\\t \\\"";
        rs += GroupID[i];
        rs += "\\\": {\\n";
        rs += "\\t \\\"Pwd\\\": \\\"";
        rs += key[i];
        rs += "\\\"\\n";
        rs += "\\t}\\n";

    rs += "}";

    return rs;

def MakeCodeForPhysicalKeyAsKeyboard(filename):
    if not os.path.exists(filename):
      os.makedirs(filename)
    f = open("./" + filename + "/" + filename+ ".ino", "w")
    code = []
    f.write("#include \"DigiKeyboard.h\"\n")
    f.write("void setup() {\n}\n")
    f.write("void loop()\n{\nDigiKeyboard.sendKeyStroke(0);\n")
    f.write("DigiKeyboard.println(\"This is property of Indian Govt.\");\n")
    code.append("DigiKeyboard.println(\"" + JsonFormatToCopy() + "\");")
    f.writelines(code)
    f.write("\nDigiKeyboard.delay(5000);\n")
    f.write("}")
    f.close()
	
def MakeCodeForPhysicalKeyAsUSB(filename):
    if not os.path.exists(filename):
      os.makedirs(filename)
    f = open("./" + filename + "/" + filename+ ".ino", "w")
    code = []
    f.write("#include <DigiUSB.h>\n")
    f.write("void setup() {\nDigiUSB.begin();\n")
    f.write("DigiUSB.delay(1000);\n")
    f.write("DigiUSB.println(\""+ JsonFormatToCopy() +"\");")
    f.write("}\n")
    f.write("void loop()\n{\n")
    f.write("DigiUSB.println(\"This is property of Indian Govt.\");\n")
    #code.append("DigiKeyboard.println(\"" + JsonFormatToCopy() + "\");")
    #f.writelines(code)
    f.write("DigiUSB.delay(5000);\n")
    f.write("}")
    f.close()

if __name__ == '__main__':
    MakeCodeForPhysicalKeyAsUSB("Person1")