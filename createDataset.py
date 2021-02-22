import os
import shutil

sub_dir = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

result_dir = './results'
result_subdir = './results/'
if not os.path.exists(result_dir):
    os.mkdir(result_dir)
    for i in range(len(sub_dir)):
        os.mkdir(result_subdir + '/' + sub_dir[i])

for dir_name in sub_dir:
    target_dir = './MMAFEDB/train/' + dir_name
    fltr_list = [filename for filename in os.listdir(target_dir) if not filename.startswith('.')]

    for i in range(50):
        newImgName = dir_name + '_' + str(i).zfill(2)
        shutil.copyfile(target_dir+'/'+fltr_list[i], './results/'+dir_name+'/'+newImgName+'.jpg')
