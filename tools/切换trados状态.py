from itertools import chain
from xml.etree import ElementTree
import os

for root, _, files in os.walk("."):
    for file in files:
        if file == "LocalizationDef.json.sdlxliff":
            tempPath = os.path.join(root, file)
            with open(tempPath, "r+", encoding="utf-8") as f:
                tempStr= f.read()
                newStr = tempStr.replace("ApprovedTranslation", "Translated")
                f.truncate(0)
                f.seek(0)
                f.write(newStr)