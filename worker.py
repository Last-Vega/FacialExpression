import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calc_workers_enthusiasm(f):
    df = pd.read_csv(f)
    label_list = []
    for url in df['Input.image_url']:
        # print(url)
        label_list.append(url.split('/')[-1].split('_')[0])

    df['label'] = label_list

    dict = {}
    workers = df['WorkerId']

    for worker, label, prediction in zip(df['WorkerId'], df['label'], df['Answer.category.label']):
        if worker not in dict.keys():
            # dict[worker] = 1
            dict[worker] = [0, 0, 0]
            dict[worker][0] = 1
            dict[worker][1] = 0
        else:
            dict[worker][0] += 1

        if label == prediction:
            dict[worker][1] += 1


    scatter_x = []
    scatter_y = []
    for key, value in dict.items():
        if value[0] != 0:
            value[2] = value[1] / value[0]
        else:
            value[2] = 0
        scatter_x.append(value[2])
        scatter_y.append(value[0])
    x = np.array(scatter_x)
    y = np.array(scatter_y)
    plt.scatter(x, y, color="green")
    # plt.scatter(x, y, color="blue")
    plt.title("Scatter plot of number of responses and percentage of correct answers")
    plt.xlabel("percentage of correct answers")
    plt.ylabel("Number of answers")
    # plt.grid(True)

    plt.show()

    fig = plt.figure()
    fig.savefig("worker-1.png")
    # fig.savefig("worker-2.jpg")
    # print(f, 'workers', dict)


    # print(sum(dict.values()))

calc_workers_enthusiasm('./Batch_4350992_batch_results.csv')
# calc_workers_enthusiasm('./Batch_4369243_batch_results.csv')
