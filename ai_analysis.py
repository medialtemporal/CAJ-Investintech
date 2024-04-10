import csv

ai_values = {}

with open('ai_data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        faculty = row[0].split('/')[0]
        row[1] = row[1].strip('[]')
        if faculty not in ai_values:
            if row[1]:  # Empty string is falsy
                ai_values[faculty] = [1, 1]  # 1 value, 0 mention AI
            else:
                ai_values[faculty] = [1, 0]  # 1 value, 0 mention AI
        else:
            if row[1]:
                ai_values[faculty][1] += 1  # Add 1 value for mention AI
            ai_values[faculty][0] += 1


print(ai_values)

