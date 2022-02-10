import os
from modules.langs import hi
from modules.constants import Constants


if __name__ == "__main__":
    obj = hi.ITN()

    file_path = (
        "/media/reverie-pc/bigdata/rohnak/indic-ITN/sample_data/sample_input.txt"
    )

    with open(
        os.path.join(Constants.ROOT_PATH, "sample_data", "output.txt"), "wb"
    ) as outf:
        with open(file_path) as f:
            for line in f.readlines():
                astr = obj.execute(line)
                line = f"{line} -> {astr}"
                print(line)
                line += "\n"
                outf.write((line).encode())
