class Utils:
    def file_size(size):
        number = float(size)
        count = 0
        type = ["B","kB","MB","GB"]
        while number >= 1024:
            number/=1024
            count+=1
        return ("{:.2f}".format(number)+" "+type[count]).replace(".",",")