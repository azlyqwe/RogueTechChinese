#-*-coding:utf-8-*-

from distutils.command.build import build
import os
import json

from collections import OrderedDict
for root, _,files in os.walk("./build/output"):
    for file in files:
        if file == "LocalizationDef.json":
            distPath = os.path.join(root, file)[15:]
            distPath = os.path.join("./gettext", distPath)
            if not os.path.exists(distPath[:-21]):
                os.makedirs(distPath[:-21])
            print(distPath[:-21])
            distPath = distPath.replace("json","po")
            with open(os.path.join(root, file), 'r', encoding="utf-8") as f, open(distPath, 'w', encoding="utf-8") as gettext:
                sorBuffer = json.load(f, object_pairs_hook=OrderedDict)
                for eum in sorBuffer:
                    idstr = eum["id"]
                    strstr = eum["content"]
                    gettext.write(f"migid \"{idstr}\"\n")
                    gettext.write(f"migstr \"{strstr}\"\n")


