#-*- encoding=utf8 -*-
import os
import shutil
import tarfile
import compileall

def tar_dir(tar_path):

    dstname = tar_path+'.tar.gz'
    file_name = tar_path.split('/')[-1]
    os.chdir(tar_path.split(file_name)[0])
    tarHandle=tarfile.open(dstname,"w:gz")
    try:
        for dirpath,dirs,files in os.walk(tar_path):
            for filename in files:
                tarHandle.add(os.path.join(file_name+dirpath.split(file_name)[-1],filename))
        tarHandle.close()
        return dstname
    except:
        return False

def compile(source,target):

    compileall.compile_dir(source)

    copyPyc(source,target)


sourceDir = {
    #source目录下的无效文件夹
    "sourceInvalidDir" : ["__pycache__"],
}
def delFiles(source):
    for root , dirs, files in os.walk(source):
        for dir in dirs:
            if dir in sourceDir["sourceInvalidDir"]:
                shutil.rmtree(os.path.join(root, dir))
                print ("Delete Dir: " + os.path.join(root, dir))

def copyPyc(source,target):

    files= os.listdir(source) #得到文件夹下的所有文件名称
    for file in files: #遍历文件夹
        if str(file).endswith('.ini'):
            shutil.copyfile(os.path.join(source,file),os.path.join(target,file))
        dir = os.path.join(source, file)
        if os.path.isdir(dir): # 如果是文件夹
            target_dir=os.path.join(target,file)
            if(not os.path.exists(target_dir)):
                if(not os.path.basename(target_dir)=='__pycache__'):
                    os.makedirs(target_dir)

            if(os.path.basename(dir)=='__pycache__'):
                for pyc_file in os.listdir(dir):
                    real_target_dir=str.replace(target,'__pycache__','')
                    real_pyc_file=str.split(pyc_file,".")[0]+".pyc"
                    shutil.copyfile(os.path.join(dir,pyc_file),os.path.join(target,real_pyc_file))
            else:
                copyPyc(dir,target_dir)    # 递归执行


if __name__ == "__main__":

    abspath = os.path.abspath(__file__)
    source = str(abspath.split('/auto-pyc.py')[0]) + '/dataexa-dl-v5'
    target = str(abspath.split('/auto-pyc.py')[0]) + '/dataexa-dl-v5-pyc'

    delFiles(source)    # 删除掉所有 __pycache__

    if not os.path.exists(target):
        os.mkdir(target)
    compile(source,target)
    tar_dir(target)
    #压缩完成后，删除源文件夹
    if os.path.exists(target):
        shutil.rmtree(target)
