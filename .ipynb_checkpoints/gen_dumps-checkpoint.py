def listdir_nohidden(path):
    import os
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def gen_dumps():
    import os

    # generating jellyfish command for each file containing one cluster
    work = os.getcwd()
    if not os.path.exists('./dumps/'):
        os.mkdir('./dumps/')
    dirs = listdir_nohidden(work+'/dumps')
    os.chdir(work+'/dumps')
    n = 0
    for i in dirs:
        n+=1
        if n%500==0:
            print(n)

    # executing these commands iteratively
        os.system(f'jellyfish dump {i} > ../real_dumps/{i[:-9]}.fa')

    
