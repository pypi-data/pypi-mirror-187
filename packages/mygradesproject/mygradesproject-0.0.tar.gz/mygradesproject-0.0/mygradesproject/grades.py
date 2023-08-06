def calculate_grade(marks):
    if marks >= 90:
        grade = 'A'
        weightage = 4.0
    elif marks >= 80:
        grade = 'B'
        weightage = 3.0
    elif marks >= 70:
        grade = 'C'
        weightage = 2.0
    elif marks >= 60:
        grade = 'D'
        weightage = 1.0
    else:
        grade = 'F'
        weightage = 0.0
    return grade, weightage

def calculate_gpa(marksList):
    total_weightage = 0
    credits = 0
    for grade in marksList:
        grade, weightage = calculate_grade(grade)
        total_weightage += weightage
        credits += 1
    gpa = total_weightage / credits
    return gpa
# print(calculate_grade(75))
print(calculate_gpa([100,90,50,75,100]))