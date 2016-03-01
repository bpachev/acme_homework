import sqlite3 as sql
import csv

#I want to work with the same connection and cursor throughout the entire script.
db = sql.connect("student_information_bpachev")
cur = db.cursor()

def prob1():
 #StudentID to StudentName is one-to-one. Each ID maps into a distinct name. Students is the table involved.
 #MajorCode to studentId is one-to-many, as multiple students can have the same major. Students and Subjects are involved.
 #ClassId to Grade is many-to-many. Students, Grades, and Classes are involved.
 #StudentID to Grade is many-to-many. Classes, Grades, and Students are involved.
 #StuentID to ClassID is many-to-many. Each class has multiple students, and each student can have more than one class. Classes, Grades and Students are involved
 pass

def init():
 global db,cur
 #I know this function is exploitable
 #Think of it as an internal sub-routine only.
 def load_csv(tblname,filename,num_fields):
  query = "INSERT INTO "+str(tblname)+" VALUES("+",".join(["?"]*num_fields)+")"
  with open(filename,"r") as csvfile:
   for row in csv.reader(csvfile,delimiter=","):
    for i, el in enumerate(row):
     if "NULL" in el:
      row[i] = None
    cur.execute(query,row)
 tbls = [("students",4),("grades",3),("classes",2),("majors",2)]
 cur.execute("DROP TABLE if exists students")
 cur.execute("DROP TABLE if exists grades")
 cur.execute("DROP TABLE if exists classes")
 cur.execute("DROP TABLE if exists majors")
 cur.execute("CREATE TABLE students (StudentID int, StudentName String,MajorSubjectID int,MinorSubjectId int)")
 cur.execute("CREATE TABLE grades (StudentID int,ClassId int,Grade string)")
 cur.execute("CREATE TABLE classes (ClassID int,Name string)")
 cur.execute("CREATE TABLE  majors (MajorId int,MajorName string)")
 for tbl,ncols in tbls:
  load_csv(tbl,tbl+".csv",ncols)
  cur.execute("SELECT * FROM "+tbl)

init() 
 
def prob2():
 global cur
 cur.execute("SELECT MajorName,COUNT(*) num_students from students s left outer join majors m on s.MajorSubjectID=m.MajorID GROUP BY m.MajorID ORDER BY MajorName")
 return cur.fetchall()

def prob3():
 global cur
 cur.execute("SELECT s.StudentID,StudentName,COUNT(*) num_grades from students s join grades g on s.StudentID = g.StudentID where g.grade is not null GROUP BY s.StudentID HAVING(num_grades)>=2")
 return cur.fetchall()

def prob4():
 global cur
 case_expr = "CASE grade "
 grds = ["A","B","C","D"]
 for i,grd in enumerate(grds):
  gp = 4.0-i
  case_expr += "WHEN '"+grd+"' THEN %f " % gp
  case_expr += "WHEN '"+grd+"+' THEN %f " % gp
  case_expr += "WHEN '"+grd+"-' THEN %f " % gp
 case_expr += "ELSE 0.0 END"
 cur.execute("SELECT ROUND(AVG(("+case_expr+")),2) from grades where grade is not null")
 return cur.fetchall()[0][0]

