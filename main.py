import os
from modules.langs import hi
from modules.constants import Constants

if __name__ == "__main__":
    obj = hi.Hi()

    file_path = "/media/reverie-pc/bigdata/rohnak/indic-ITN/sample_input.txt"

    with open(os.path.join(Constants.ROOT_PATH, "output.txt"), "wb") as outf:
        with open(file_path) as f:
            for line in f.readlines():
                s, astr = obj.execute(line, to_eng=True)
                outf.write((f"{s} -> {astr}\n").encode())
