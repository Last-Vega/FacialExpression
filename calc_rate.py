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

print(correct/count)
