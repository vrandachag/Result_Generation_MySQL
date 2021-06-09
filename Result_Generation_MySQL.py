import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
from datetime import date

def count(list1, l, r):
    c = 0 
    # traverse in the list1
    for x in list1:
        # condition check
        if x>= l and x<= r:
            c+= 1 
    return c
def Return_Grade(g1,max_marks):
    marks = (g1/max_marks)*100
    if marks >= 80 and marks <=100:
        return 'A'
    elif marks >= 75 and marks <=79.9:
        return 'B+'
    elif marks >= 65 and marks <= 74.9:
        return 'B'
    elif marks >= 55 and marks <= 64.9:
        return 'C+'
    elif marks >= 50 and marks <=54.9:
        return 'C'
    elif marks >= 40 and marks <= 49.9:
        return 'D'
    else:
        return 'F'

#Report
def Result_Display():
    global mydb
    mycursor = mydb.cursor()

    sn = input("Enter Scholar Number:")
    term = input("Enter Term:")

    sql = f"SELECT \
            student_details.Student_Name,student_marks.Scholar_Number,student_marks.Subject_Code,subjects.Subject_Name, student_marks.Marks_Obtained, student_marks.Max_Marks,student_marks.Section, student_marks.Term, student_marks.S_year,student_marks.Year \
            FROM student_details \
            JOIN student_marks \
            ON student_marks.Scholar_Number = {sn} AND student_marks.Term = {term} AND student_details.scholar_number = student_marks.scholar_number \
            JOIN subjects \
            WHERE student_marks.subject_code = subjects.subject_code;" 
                        
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    flag = 0
    total = 0
    count = 0
    avg = 0
    pass_1 = 1
    myTable = PrettyTable(["Subject Code","Subject Name","Marks Obtained","Max Marks","Grade"])
    for x in myresult:
        if flag == 0:
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("Name:" + x[0])
            print("Enrollment Number:" + str(x[1]))
            print("Term:" + x[7])
            print("Section:" + x[6])
            print("Sessional Year:" + x[8])
            print("Year:" + x[9])
            flag = -1
        l = []
        l.append(x[2])
        l.append(x[3])
        l.append(x[4])
        l.append(x[5])
        pORf = Return_Grade(x[4],x[5])
        l.append(pORf)
        if pORf == 'F':
            pass_1 = 0
        avg = avg + x[4]
        total = total + x[5]
        count = count + 1
        
        myTable.add_row(l)

    print(myTable)
    print("Average:" + str(avg/count))
    print("Grade:" + Return_Grade(avg,total))
    if pass_1 != 0:
        print("Status:PASS")
    else:
        print("Status:FAIL")

#transaction
def Marks_insert():   
    global mydb
    mycursor = mydb.cursor()

    subject = input("Enter subject:")
    term = input("Enter term:")
    s_yr = input("Enter current year:")
    dept = input("Enter department:")
    section = input("Enter section:")
    max_marks = input("Input enter maximum marks:")
    yr = input("Enter year:")
    sql = f" SELECT subjects.subject_code \
    FROM subjects \
    WHERE subjects.subject_name = '{subject}' " 

    mycursor.execute(sql)

    marks = mycursor.fetchall()
    
    for i in marks:
        print(i)
        sql1 = f"SELECT sd.scholar_number,sd.student_name \
            FROM student_details sd,student_subject_details ssd \
            WHERE sd.scholar_number = ssd.scholar_number AND sd.current_section = '{section}' AND \
            (ssd.subject_code_1 = '{i[0]}' OR \
            ssd.subject_code_2 = '{i[0]}' OR \
            ssd.subject_code_3 = '{i[0]}' OR \
            ssd.subject_code_4 = '{i[0]}' OR \
            ssd.subject_code_5 = '{i[0]}' OR \
            ssd.subject_code_6 = '{i[0]}'); "

        mycursor.execute(sql1)

        name = mycursor.fetchall()
        flag = 0
        for m1 in name:
            print("Scholar Number:" + str(m1[0]))
            print("Name:" + m1[1])
            inp_marks = input("Enter marks:")
            sql2 = f"INSERT INTO student_marks(Scholar_Number,Subject_Code,Marks_obtained,Max_Marks,Department,Section,Term,S_Year,Year) \
                VALUES(%s,%s,{inp_marks},{max_marks},'{dept}','{section}',{term},{s_yr},{yr})"
            l1 = (m1[0],i[0])
            mycursor.execute(sql2,l1)
            mydb.commit()

#Master Data
def Add_scholar(): 
        global mydb
        mycursor = mydb.cursor()
        name = input("Enter Name:")
        Address = input("Enter Address:")
        FN = input("Enter Fathers name:")
        MN = input("Enter Mother's name:")
        dob = input("Enter date of birth(YYYY-MM-DD):")
        mob_no = input("Enter mobile number:")
        pincode = input("Enter pincode:")
        BG = input("Enter blood group:")
        dept = input("Enter department:")
        
        date_today = date.today()
        print(date_today)
        enroll_yr = input("Enter addmission year:")
        current_yr = input("Enter current year:")
        section = input("Enter section:")    
        
        insert_into_student = f"INSERT INTO student_details \
                               (Student_Name,Student_Address,Fathers_Name,Mothers_Name,DOB,Mobile_Number,Pincode,Blood_Group,Department,Date_of_Addmission,Enrolling_S_Year,Current_S_Year,Current_Section) \
                                VALUES('{name}','{Address}','{FN}', '{MN}', '{dob}' , '{mob_no}','{pincode}','{BG}','{dept}','{date_today}',{enroll_yr},{current_yr},'{section}');"
        mycursor.execute(insert_into_student)
        mydb.commit()

#Master Data
def Add_Subject(): 
    global mydb
    mycursor = mydb.cursor()
    sub_code = input("Enter subject code:")
    sub_name = input("Enter subject name:")

    insert_subject = f"INSERT INTO subjects \
                     (Subject_Code,Subject_Name) \
                     VALUES('{sub_code}','{sub_name}') ;"
    mycursor.execute(insert_subject)
    mydb.commit()

#Master Data
def Assign_Subject_Students():
    global mydb
    flag = 1
    mycursor = mydb.cursor()
    SN = input("Enter Scholar Number:")
    dept = input("Enter department:")
    section = input("Enter section:")
    term = input("Enter term:")

    subject_name = []
    for i in range(0,6):
        while flag == 1:
            s_name = input("Enter subject name:")
            if s_name not in subject_name:
                subject_name.append(s_name)
                flag = 0
            else:
                print("Subject present already!!")
        choice = input("Want to enter more?(Y/N):")
        if choice.upper() == 'N':
            break
        else:
            flag = 1
    while len(subject_name) < 6:
        subject_name.append("No Subject")

    subject_code =[]
    for i in range(0,6):
        fetch_sub_code = f"SELECT Subject_Code \
                         FROM Subjects \
                         WHERE Subject_Name = '{subject_name[i]}'"
        mycursor.execute(fetch_sub_code)
        scode = mycursor.fetchall()
        for x1 in scode:
            subject_code.append(x1[0])
    print(subject_code)
        
    print(subject_code)
    insert_student_subject_details = f"INSERT INTO student_subject_details \
                                     VALUES({SN},'{subject_code[0]}','{subject_code[1]}','{subject_code[2]}','{subject_code[3]}','{subject_code[4]}','{subject_code[5]}','{dept}','{section}',{term});"
    mycursor.execute(insert_student_subject_details)
    mydb.commit()

def Modify_Student_Data():
    global mydb
    mycursor = mydb.cursor()

    ch = 'Y'
    while ch.upper() == 'Y':
        new_entry = ''
        sn = input("Enter scholar number:")
        print("1.Update Address")
        print("2.Update Father's Name")
        print("3.Update Mother's Name")
        print("4.Update Mobile Number")
        print("5.Update Current Year")
        print("6.Update Current Section")
        choice = int(input("Enter choice(1-7):"))
        if choice == 1:
            new_entry = input("Enter new address:")
            update = f"UPDATE student_details \
                     SET Student_Address = '{new_entry}' \
                     WHERE Scholar_Number = {sn};"
        elif choice == 2:
            new_entry = input("Enter Father's Name:")
            update = f"UPDATE student_details \
                     SET Fathers_Name = '{new_entry}' \
                     WHERE Scholar_Number = {sn};"
        elif choice == 3:
            new_entry = input("Enter Mother's Name:")
            update = f"UPDATE student_details \
                   SET Mothers_Name = '{new_entry}' \
                   WHERE Scholar_Number = {sn};"
        elif choice == 4:
            new_entry = input("Enter new Mobile Number:")
            update = f"UPDATE student_details \
                   SET Mobile_Number = '{new_entry}' \
                   WHERE Scholar_Number = {sn};"
        elif choice == 5:
            new_entry = input("Enter Current Year:")
            update = f"UPDATE student_details \
                   SET Current_S_Year = '{new_entry}' \
                   WHERE Scholar_Number = {sn};"
        elif choice == 6:
            new_entry = input("Enter Current Section:")
            update = f"UPDATE student_details \
                   SET Current_Section = '{new_entry}' \
                   WHERE Scholar_Number = {sn};"
        mycursor.execute(update)
        mydb.commit()
        ch = input("Want to modify more details?(Y/N):")

#Master Data
def Modify_Subjects_Data():
    global mydb
    mycursor = mydb.cursor()

    ch = 'Y'
    while ch.upper() == 'Y':
        new_entry = ''
        sn = input("Enter Subject Code:")
        print("Update Subject Name")
        new_entry = input("Enter new Subject Name:")
        update = f"UPDATE subjects \
                 SET Subject_Name = '{new_entry}' \
                 WHERE Subject_Code = '{sn}';"
        mycursor.execute(update)
        mydb.commit()
        ch = input("Want to modify more details?(Y/N):")

#Transaction
def Update_Marks():
    global mydb
    mycursor = mydb.cursor()

    sub_name = input("Enter subject name:")
    max_marks = input("Enter maximum marks:")
    dept = input("Enter Department:")
    section = input("Enter section:")
    term = input("Enter term:")
    s_yr = input("Enter current sessional year:")
    yr = input("Enter year:")

    get_sub_code = f"SELECT Subject_Code \
                   FROM Subjects \
                   WHERE Subject_Name = '{sub_name}' "
    mycursor.execute(get_sub_code)
    sub_code = mycursor.fetchall()

    for sub in sub_code:
        student = f"SELECT ssd.Scholar_Number,sd.Student_Name \
                  FROM student_details sd, student_subject_details ssd \
                  WHERE sd.Scholar_Number = ssd.Scholar_Number AND sd.Department = '{dept}' AND sd.Current_Section = '{section}' AND \
                  sd.Department = ssd.Department AND ssd.Term = {term} AND \
                  (ssd.Subject_Code_1 = '{sub[0]}' OR \
                  ssd.Subject_Code_2 = '{sub[0]}' OR \
                  ssd.Subject_Code_3 = '{sub[0]}' OR \
                  ssd.Subject_Code_4 = '{sub[0]}' OR \
                  ssd.Subject_Code_5 = '{sub[0]}' OR \
                  ssd.Subject_Code_6 = '{sub[0]}')  ;"
        mycursor.execute(student)
        student1 = mycursor.fetchall()

        for s in student1:
          check_entry = f"SELECT Scholar_Number \
                        FROM Student_Marks \
                        WHERE Subject_Code = '{sub[0]}' AND Max_Marks = {max_marks} AND Department = '{dept}' AND Section = '{section}' AND \
                        Term = {term} AND S_Year = {s_yr} AND Year = {yr};"
          mycursor.execute(check_entry)
          chk = mycursor.fetchall()

          for c1 in chk:
              if s[0] in c1:
                  print("Marks already inserted")
                  break
          else:
              if len(chk) == 0:
                  print("Scholar Number:" + str(s[0]))
                  print("Name:" + s[1])
                  marks = input("Enter Marks:")
                  insert_marks = f"INSERT INTO student_marks \
                                   VALUES({s[0]},'{sub[0]}',{marks},{max_marks},'{dept}','{section}',{term},{s_yr},{yr});"
                  mycursor.execute(insert_marks)
                  mydb.commit()

def Analysis_Subject():
    global mydb
    mycursor = mydb.cursor()
    dept = input("Enter Department:")
    sub_name = input("Enter Subject Name:")
    term = input("Enter term:")
    s_year = input("Enter Current Sessional Year:")
    section = input("Enter section:")
    yr = input("Enter year:")

    sub_code = f"SELECT Subject_Code \
               FROM Subjects \
               WHERE Subject_Name = '{sub_name}';"
    mycursor.execute(sub_code)
    code = mycursor.fetchall()

    for sub in code:
        students = f"SELECT Marks_Obtained,Max_Marks \
                   FROM student_marks \
                   WHERE Department = '{dept}' AND Subject_Code = '{sub[0]}' \
                   AND Section = '{section}' AND Term = {term} AND S_Year = {s_year} \
                   AND Year = {yr};"
    mycursor.execute(students)
    marks = mycursor.fetchall()
    print(marks)
    percent = []
    for m1 in marks:
      p1 = round(((m1[0]*100)/m1[1]),2)
      print(p1)
      percent.append(p1)

    range_list = []
    for i in range(0,100,20):
      range_list.append(count(percent,i,i+20))

    print(range_list)
    y = np.array(range_list)
    mylabels = ["A+","A","B+","B","C"]

    plt.pie(y,labels = mylabels)
    plt.legend(title = "Grades:")
    plt.title("Subject wise Student Analysis")
    plt.show()

#ask
def Analysis_Term():
    global mydb
    mycursor = mydb.cursor()
    dept = input("Enter Department:")
    term = input("Enter term:")
    s_year = input("Enter Current Sessional Year:")
    section = input("Enter section:")
    yr = input("Enter year:")
    total_students = 8

    N = 5 #Grade division
    ind = np.arange(N)
    width = 0.25
    '''
    ts = f"SELECT DISTINCT COUNT(*) \
                        FROM student_marks \
                        WHERE department = '{dept}' AND term = '{term}' AND S_Year = '{s_year}' \
                        AND section = '{section}' AND YEAR = '{yr}';"
    mycursor.execute(ts)
    s1 = mycursor.fetchall()
                        
    for total_students in s1:            
        dis_sub = f"SELECT DISTINCT Subject_Code \
                    FROM student_marks \
                    WHERE department = '{dept}' AND term = '{term}' AND S_Year = '{s_year}' \
                    AND section = '{section}' AND YEAR = '{yr}';"
        mycursor.execute(dis_sub)
        sub = fetchall()
    '''
    print("AI")
    val1 = f"SELECT Marks_Obtained,Max_Marks \
            FROM student_marks \
            WHERE Department = '{dept}' AND Subject_Code = 'CS3EAI' \
            AND Section = '{section}' AND Term = {term} AND S_Year = {s_year} \
            AND Year = {yr};"
    mycursor.execute(val1)
    marks1 = mycursor.fetchall()

    print(marks1)
    percent1 = []
    for m1 in marks1:
        p1 = round(((m1[0]*100)/m1[1]),2)
        print(p1)
        percent1.append(p1)

    range_list1 = []
    for i in range(0,100,20):
        student_percent = ( count(percent1,i,i+20) * 100)/total_students  
        range_list1.append(student_percent)
    print(range_list1)
    
    print("CP-2")
    val2 = f"SELECT Marks_Obtained,Max_Marks \
            FROM student_marks \
            WHERE Department = '{dept}' AND Subject_Code = 'CS3CP2' \
            AND Section = '{section}' AND Term = {term} AND S_Year = {s_year} \
            AND Year = {yr};"
    mycursor.execute(val2)
    marks2 = mycursor.fetchall()

    print(marks2)
    percent2 = []
    for m1 in marks2:
        p1 = round(((m1[0]*100)/m1[1]),2)
        print(p1)
        percent2.append(p1)

    range_list2 = []
    for i in range(0,100,20):
        student_percent = ( count(percent2,i,i+20) * 100)/total_students   
        range_list2.append(student_percent)
    print(range_list2)

    print("DBMS")
    val3 = f"SELECT Marks_Obtained,Max_Marks \
            FROM student_marks \
            WHERE Department = '{dept}' AND Subject_Code = 'CS3DB' \
            AND Section = '{section}' AND Term = {term} AND S_Year = {s_year} \
            AND Year = {yr};"
    mycursor.execute(val3)
    marks3 = mycursor.fetchall()

    print(marks3)
    percent3 = []
    for m1 in marks3:
        p1 = round(((m1[0]*100)/m1[1]),2)
        print(p1)
        percent3.append(p1)

    range_list3 = []
    for i in range(0,100,20):
        student_percent = ( count(percent3,i,i+20) * 100)/total_students   
        range_list3.append(student_percent)
    print(range_list3)

    bar1 = plt.bar(ind,range_list1,width,color = 'r')
    bar2 = plt.bar(ind+width,range_list2,width,color = 'g')
    bar3 = plt.bar(ind+width*2,range_list3,width,color = 'b')
    
    plt.xlabel("Subjects")
    plt.ylabel("Marks Percent")
    plt.title("Term Wise Student Analysis")

    plt.legend(ind+width,['AI','CP-2','DBMS'])
    plt.show()

    
mydb = mysql.connector.connect(
host = "localhost",
database = "student_record_system",
user = "root",
password = "Helloworld123"
    #    password = input("Enter password:"),
)


ch = 'Y'
while ch.upper() == 'Y':
    print("1.Master Data")
    print("2.Transaction")
    print("3.Reports")
    print("4. Exit")
    choice = int(input("Enter choice(1-4):"))
    if choice == 1:
        print("MASTER DATA!")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("1.Add New Scholar")
        print("2.Add New Subject")
        print("3.Assign Subjects to Students")
        print("4.Modify Student Data")
        print("5.Modify Subject Data")
        print("6.Exit")
        ch1 = int(input("Enter choice:"))
        if ch1 == 1:
          Add_scholar()
        elif ch1 == 2:
          Add_Subject()
        elif ch1 == 3:
          Assign_Subject_Students()
        elif ch1 == 4:
          Modify_Student_Data()
        elif ch1 == 5:
          Modify_Subjects_Data()
       # else:
        #    break
    elif choice == 2:
        print("TRANSACTIONS!")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("1.Insert Marks")
        print("2.Update Marks")
        print("3.Exit")
        ch2 = int(input("Enter choice(1-3):"))
        if ch2 == 1:
            Marks_insert()
        elif ch2 == 2:
            Update_Marks()
    #    else:
     #       break
    elif choice == 3:
        print("REPORTS!")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("1.Display Result")
        print("2.Result Analysis")
        print("3.Exit")
        ch3 = int(input("Enter choice(1-3):"))
        if ch3 == 1:
            Result_Display()
        elif ch3 == 2:
            print("\n\n\nAnalysis!")
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("1.Subject wise Analysis")
            print("2.Term wise Analysis")
            print("3.Back")
            ch3_1 = int(input("Enter choice(1-3):"))
            if ch3_1 == 1:
                Analysis_Subject()
            elif ch3_1 == 2:
                Analysis_Term()
    ch = input("Want to enter more?(Y/N):")

mydb.close()
