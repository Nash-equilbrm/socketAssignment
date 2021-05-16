import os


def get_file_list(path):
    os.system("cs "+ path)
    os.system("rename *.xlsx *.csv")
    files = os.listdir(path)
    csv_files = []
    for file in files:
        x = len(file) - 4
        if file[x:] == '.csv':
            csv_files.append(file)
    return csv_files
    



def func(filename, del_this_row):
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        i = 0
        for line in lines:
            i += 1
            if i!=del_this_row:
                f.write(line)


path = input("Nhap path chua cac file excel vao day: ")
list_file = get_file_list(path)
for file in list_file:
    func(file,25)



            