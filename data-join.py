import glob

data_file = "Data/*.csv"

with open("Wuhan-2019-nCoV.csv", "w", encoding="utf-8") as w:
    w.write("date,country,countryCode,province,provinceCode,city,cityCode,confirmed,suspected,cured,dead\n")
    for f in sorted(glob.glob(data_file)):
        with open(f, 'r', encoding="utf-8") as file:
            header = True
            for line in file:
                if header:
                    header = False
                else:
                    w.write(line)