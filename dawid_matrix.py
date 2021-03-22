import pandas as pd

def dawid_confusion(f1, f2):
    feelings = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprise': 6}

    f_dict = {  'angry': [0, 0, 0, 0, 0, 0, 0],
                'disgust': [0, 0, 0, 0, 0, 0, 0],
                'fear': [0, 0, 0, 0, 0, 0, 0],
                'happy': [0, 0, 0, 0, 0, 0, 0],
                'neutral': [0, 0, 0, 0, 0, 0, 0],
                'sad': [0, 0, 0, 0, 0, 0, 0],
                'surprise': [0, 0, 0, 0, 0, 0, 0]
            }

    df1 = pd.read_csv(f1)
    label_list = []
    for url in df1['Input.image_url']:
        # print(url)
        label_list.append(url.split('/')[-1].split('_')[0])

    df1['label'] = label_list
    df1 = df1[['HITId', 'label']]
    df1 = df1.drop_duplicates()

    df2 = pd.read_csv(f2, delimiter='\t')
    df2 = df2.rename(columns = {'TaskID':'HITId'})

    df = pd.merge(df1, df2, on='HITId', how='inner' )


    for label, answer in zip(df['label'], df['Estimate_label']):
        index = feelings[answer]
        f_dict[label][index] += 1

    confusion_matrix = pd.DataFrame(f_dict)
    new_index = {0: 'angry', 1: 'disgust', 2: 'fear', 3:'happy', 4:'neutral', 5:'sad', 6:'surprise'}
    confusion_matrix = confusion_matrix.rename(index = new_index)

    if f1 == './Batch_4350992_batch_results.csv':
        f_name = 'confusion-dawid-1.csv'
    else:
        f_name = 'confusion-dawid-2.csv'
    confusion_matrix.to_csv(f_name)

    return confusion_matrix

print(dawid_confusion('./Batch_4369243_batch_results.csv', './class_for_ds-1.tsv'))
