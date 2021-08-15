import os

PATH = 'helpers/log.txt'
PATH2 = 'log.txt'

async def add_to_log(description):
    global PATH
    global PATH2

    PATH_EXIST = os.path.isfile(PATH)
    PATH2_EXIST = os.path.isfile(PATH2)
    
    if not PATH_EXIST and not PATH2_EXIST:
        print('Cant find path')
        return
    if PATH_EXIST:
        PATH = PATH
    else:
        PATH = PATH2
        
    with open(PATH ,'a') as f:
        f.write('\n' + description)
    f.close()