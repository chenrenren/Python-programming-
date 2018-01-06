

Questions

Output a list of students born between June 16, 1991 and September 15, 1996
Output the number of students born between June 16, 1991 and September 15, 1996
Output a list of students who have missed one or more labs (Score <= 0.1 to avoid numeric truncation errors)
Output the name of the student with the best score at the final
Output the name of the student closest to the average score of midterm 1
Output the accumulated homework score (sum of all assignment-type score) for the students identified in 4. and 5., respectively.  
Create a VIEW named altAssignments, listing Assignment.ID, Assignment.name, Type.name, and sorted by Type.name.  For reporting use
    sqlite3> SELECT * FROM altAssignments;
and provide the output of 
    sqlite3> .schema altAssignment 
and explain what it tells you.
Create a series of INSERT statements that create a user entry for yourself, full score on all homeworks, 80% on Midterm 1, 90% on Midterm 2, and 99% on the Final.  Show all the newly added information through SELECT statements on the respective tables (make sure to design those SELECT statements to filter only those showing data for your record)
Hint: you can set sqlite3 (sqlite3.exe on windows) to load commands from a file and write all output to another file.  This can be extremely useful for documentation.
