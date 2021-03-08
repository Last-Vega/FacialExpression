import os
import shutil

sub_dir = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

result_dir = './data/test'
result_subdir = './data/test'
if not os.path.exists(result_dir):
    os.mkdir(result_dir)

for dir_name in sub_dir:
    target_dir = './MMAFEDB/test/' + dir_name
    fltr_list = [filename for filename in os.listdir(target_dir) if not filename.startswith('.')]

    for i in range(10):
        newImgName = dir_name + '_' + str(i).zfill(2)
        shutil.copyfile(target_dir+'/'+fltr_list[i], './data/test/'+newImgName+'.jpg')
