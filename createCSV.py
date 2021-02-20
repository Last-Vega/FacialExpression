import csv
import os

target_dir = './results/'
sub_dir = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

header = ['image_url']

with open('./amt.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for dir in sub_dir:
        dir_name = target_dir + dir + '/'
        fltr_list = [filename for filename in os.listdir(dir_name) if not filename.startswith('.')]
        fltr_list = sorted(fltr_list)
        for image in fltr_list:
            name = [image]
            writer.writerow(name)
