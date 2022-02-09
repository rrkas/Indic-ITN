from modules.langs import hi

if __name__=="__main__":
    obj = hi.Hi()

    file_path = "/media/reverie-pc/bigdata/rohnak/indic-ITN/sample_input.txt"
    with open(file_path) as f:
        for line in f.readlines():
            s, astr = obj.execute(line)
            print(f"{s} -> {astr}")
