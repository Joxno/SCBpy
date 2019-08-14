def read_all_text(path):
    f = open(path, "r")
    text = f.read()
    f.close()
    return text
