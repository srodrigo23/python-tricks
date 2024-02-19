
def generate_csv_file_from_pdf_file()->None:
    ##
    # Script to generate a csv file for Excel
    ##
    import csv
    students_file = open("students.txt", "r")
    careers = {
        "650001":"ING. ELECTROMECANICA",
        "309801":"ING. INDUSTRIAL",
        "319801":"ING. MECANICA",
        "349701":"LIC. EN MATEMATICAS",
        "439801":"ING. MATEMATICAS"
    }

    with open('students.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["codsis", "carr", "name"]
        writer.writerow(field)
        for student in students_file:
            if student is not '':
                row_data = student.strip()[::-1]
                posEsp1 = row_data.find(' ')
                row_data = row_data[posEsp1+1::]
                posEsp1 = row_data.find(' ')
                cod_sis = row_data[0:posEsp1:]
                posEsp2 = row_data.rfind(' ')
                cod_carr = row_data[posEsp2+1::]
                name = row_data[posEsp1+1:posEsp2:]
                # data = f"{cod_sis} {cod_carr} {name}"    
                writer.writerow([cod_sis, careers[cod_carr],name])


def read_file_from_classroom_data()->None:
    students_file = open("classroom.txt", "r")
    f = open("classroom_sorted.txt", "w", newline='')

    for student in students_file:
        if student is not '\n':
            name = student.strip().upper()
            name_array = name.split()
            if len(name_array) >= 3:
                name_array = name_array[-2:] + name_array[0:-2:]
            else:
                name_array = name_array[-1:] + name_array[0:-1:]
            f.write(" ".join(name_array) + '\n')
    f.close()

def get_students_from_pdf_list()->list:
    sorted_file = open("students.txt", "r")
    students=[]
    for student in sorted_file:
        if student is not '':
            # row_data = student.strip()[::-1]
            # data = row_data.split()
            # name = " ".join(data[2:-1:])
            students.append(student.strip())
    return students

def get_students_from_classrom_list()->list:
    txt_file = open("classroom_sorted.txt", "r")
    students=[]
    for student in txt_file:
        if student is not '':
            students.append(student.strip())
    return students

def diferencies_data()->list:
    official_students = get_students_from_pdf_list()
    classroom_students = get_students_from_classrom_list()
    cont = 0
    for student in classroom_students:
        if student not in official_students:
            cont+=1
            print(student)
    print(cont)
diferencies_data()