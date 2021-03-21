import pandas as pd

def worker_confusion(f):
    feelings = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprise': 6}
    # l = [0] * 7

    f_dict = {  'angry': [0, 0, 0, 0, 0, 0, 0],
                'disgust': [0, 0, 0, 0, 0, 0, 0],
                'fear': [0, 0, 0, 0, 0, 0, 0],
                'happy': [0, 0, 0, 0, 0, 0, 0],
                'neutral': [0, 0, 0, 0, 0, 0, 0],
                'sad': [0, 0, 0, 0, 0, 0, 0],
                'surprise': [0, 0, 0, 0, 0, 0, 0]
            }

    df = pd.read_csv(f)

    label_list = []
    for url in df['Input.image_url']:
        label_list.append(url.split('/')[-1].split('_')[0])
    df['label'] = label_list

    for label, answer in zip(df['label'], df['Answer.category.label']):
        index = feelings[answer]
        f_dict[label][index] += 1

    confusion_matrix = pd.DataFrame(f_dict)
    new_index = {0: 'angry', 1: 'disgust', 2: 'fear', 3:'happy', 4:'neutral', 5:'sad', 6:'surprise'}
    confusion_matrix = confusion_matrix.rename(index = new_index)

    return confusion_matrix

print(worker_confusion('./Batch_4350992_batch_results.csv'))
print('#####################')
print(worker_confusion('./Batch_4369243_batch_results.csv'))


#
#           angry  disgust  fear  happy  neutral  sad  surprise
# angry       127       28    64      2       14   19        25
# disgust      14       43    17      0       15   15        15
# fear         11       18    31      1        7   16        21
# happy        28       34    30    263       33   28        52
# neutral      51       92    51     19      164   61        31
# sad          57       74    83      6       58  156        18
# surprise     12       11    24      9        9    5       138
# #####################
#           angry  disgust  fear  happy  neutral  sad  surprise
# angry       130       27    42      2       13   25        19
# disgust      22       90    16      1       10   16        13
# fear         19       18    96      3       18   22        36
# happy        19       32    29    257       34   22        43
# neutral      52       71    41     22      177   45        22
# sad          48       57    59      6       43  169         8
# surprise     10        5    17      9        5    1       159
#
