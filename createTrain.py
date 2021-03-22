import os
import shutil

sub_dir = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

result_dir = './data2'
result_subdir = './data2/'
if not os.path.exists(result_dir):
    os.mkdir(result_dir)
    for i in range(len(sub_dir)):
        os.mkdir(result_subdir + '/' + sub_dir[i])

f = {
        'angry': 87,
        'disgust': 65,
        'fear': 74,
        'happy': 142,
        'neutral': 127,
        'sad': 118,
        'surprise': 87
    }
for dir_name in sub_dir:
    target_dir = './MMAFEDB/valid/' + dir_name
    fltr_list = [filename for filename in os.listdir(target_dir) if not filename.startswith('.')]

    count = 300 - f[dir_name]

    for i in range(count):
        newImgName = dir_name + '_augumated_' + str(i).zfill(2)
        shutil.copyfile(target_dir+'/'+fltr_list[i], './data2/train/'+dir_name+'/'+newImgName+'.jpg')
