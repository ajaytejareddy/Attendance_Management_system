import csv
import firebase as f
import time

date = time.strftime("%d") + time.strftime("%m") + time.strftime("%Y") + ".csv"

def main():
    att = csv1()
    name="Name"
    t="Total Classes"
    A="Attended"
    with open(date, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([name+","+t+","+A])
        for key in att:
            if key != 'Total Held':
                spamwriter.writerow([key+","+str(att["Total Held"])+ "," + str(att[key])])

def csv1():
    db = f.Firebase_Read()
    #print(db)

    total = 0
    total_stu = 0
    att={}

    for key in db:
        total_stu=0
        if key == 'Total Held':
            for date in db[key]:
                total = total + len(db[key][date])
            att[key]=int(total/2)
        else:
            for date in db[key]:
                total_stu = total_stu + len(db[key][date])
            att[key]=total_stu

    print(att)

    date = time.strftime("%d") + time.strftime("%m") + time.strftime("%Y")+".csv"
    return att

