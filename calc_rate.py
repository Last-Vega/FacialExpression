import csv


with open('./Batch_4350992_batch_results.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    count = 0
    correct = 0
    for row in reader:
        label = row[27].split('/')[-1].split('_')[0]
        answer = row[28]

        if label == answer:
            correct += 1
        count += 1

print(correct)
print(count)
print(correct/count)

print("####################")

with open('./Batch_4369243_batch_results.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    count = 0
    correct = 0
    for row in reader:
        # print(row[27])
        # exit()
        label = row[27].split('/')[-1].split('_')[0]
        answer = row[29]

        if label == answer:
            correct += 1
        count += 1

print(correct)
print(count)
print(correct/count)
