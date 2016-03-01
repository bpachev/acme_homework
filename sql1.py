import sqlite3 as sql
import csv

def prob1():
 db = sql.connect("test1")
 cur = db.cursor()
 #Just in case the tables already exist 
 cur.execute("DROP TABLE MajorInfo") 
 cur.execute("DROP TABLE CourseInfo") 
 cur.execute("CREATE TABLE MajorInfo (MajorCode INT NOT NULL, MajorName STRING NOT NULL)")
 cur.execute("CREATE TABLE CourseInfo (CourseID INT NOT NULL, CourseName STRING NOT NULL)")
 cur.execute("INSERT INTO CourseInfo values (436,'Model Dynamics & Control'),(402,'Model Uncertainty & Data')")
 cur.execute("SELECT * from CourseInfo")
 print cur.fetchall()
 db.close()
 

def prob2():
 #I'm trying to avoid name collisions
 db = sql.connect("benjamin_test")
 cur = db.cursor()
 #cleanup
 cur.execute("DROP TABLE if exists icd9_info")
 
 #create tables
 cur.execute("CREATE TABLE icd9_info (id INT NOT NULL, gender STRING NOT NULL, age INT NOT NULL, code STRING NOT NULL)")
 
 query = "INSERT INTO icd9_info VALUES(?,?,?,?)"
 with open("icd9.csv","r") as csvfile:
   for row in csv.reader(csvfile,delimiter=","):
     cur.execute(query,row)
   
 cur.execute("SELECT COUNT(*),gender FROM icd9_info where age <= 35 and age >= 25 GROUP BY gender")
 print cur.fetchall()
 cur.execute("SELECT * FROM icd9_info WHERE id=0")
 print cur.fetchall()

def prob3():
 students = [(401767594,"Michelle Fernandez",1),(678665086,"Gilbert Chapman",1),(553725811,"Roberta Cook",2),(886308195,"Rene Cross",3),(103066521,"Cameron Kim",4),(821568627,"Mercedes Hall",3),(206208438,"Kristopher Tran",2),(341324754,"Cassandra Holland",1),(262019426,"Alfonso Phelps",3),(622665098,"Sammy Burke",2)]
 grades = [(401767594,4,"C"),(401767594,3,"B-"),(678665086,4,"A+"),(678665086,3,"A+"),(553725811,2,"C"),(678665086,1,"B"),(886308195,1,"A"),(103066521,2,"C"),(103066521,3,"C-"),(821568627,4,"D"),(821568627,2,"A+"),(821568627,1,"B"),(206208438,2,"A"),(206208438,1,"C+"),(341324754,2,"D-"),(341324754,1,"A-"),(103066521,4,"A"),(262019426,2,"B"),(262019426,3,"C"),(622665098,1,"A"),(622665098,2,"A-")]
 majors = [(1,"Math"),(2,"Science"),(3,"Writing"),(4,"Art")] 
 classes = [(1,"Calculus"),(2,"English"),(3,"Pottery"),(4,"History")]

 db = sql.connect("benjamin_test")
 cur = db.cursor()
 cur.execute("CREATE TABLE IF NOT EXISTS students (StudentID INT not null, Name STRING, MajorCode INT not null)")
 cur.execute("CREATE TABLE IF NOT EXISTS grades (StudentID INT not null, ClassID INT not null, Grade STRING)")
 cur.execute("CREATE TABLE IF NOT EXISTS majors (ID INT not null, Name STRING)")
 cur.execute("CREATE TABLE IF NOT EXISTS classes (ClassID INT not null, Name STRING)")
 
 cur.executemany("INSERT INTO students VALUES(?,?,?);",students)
 cur.executemany("INSERT INTO grades VALUES(?,?,?);",grades)
 cur.executemany("INSERT INTO majors VALUES(?,?);",majors)
 cur.executemany("INSERT INTO classes VALUES(?,?);",classes)
 cur.execute("SELECT * FROM STUDENTS")
 print cur.fetchall() 
 db.close()

prob2()

def prob4():
 # There are 114912 women and 126953 men between the ages of 25 and 35 (inclusive).
 pass
