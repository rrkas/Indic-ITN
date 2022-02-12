import os
from modules.langs import lang_map
from modules.constants import Constants


if __name__ == "__main__":
    itn = lang_map["hi"]
    file_paths = (
        "/media/reverie-pc/bigdata/rohnak/indic-ITN/sample_data/sample_input.txt",
    )
    for file_path in file_paths:
        with open(file_path.replace(".txt", "_ITN.txt"), "wb") as outf:
            with open(file_path) as f:
                for line in f.readlines():
                    line = line.strip()
                    astr = itn.execute(line)
                    line = f"{line.strip()} -> {astr}"
                    print(line)
                    line += "\n"
                    outf.write((line).encode())
