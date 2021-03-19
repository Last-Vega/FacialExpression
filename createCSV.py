import csv
import os

target_dir = './results/'
sub_dir = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

header = ['image_url', 'label']

with open('./amt.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for dir in sub_dir:
        dir_name = target_dir + dir + '/'
        fltr_list = [filename for filename in os.listdir(dir_name) if not filename.startswith('.')]
        fltr_list = sorted(fltr_list)
        for image in fltr_list:
            base = 'https://s3-ap-northeast-1.amazonaws.com/projects.crowd4u.org/s1811552/results/'
            name = [base+dir+'/'+image, dir]
            writer.writerow(name)
