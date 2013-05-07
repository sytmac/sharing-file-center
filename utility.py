'''
Created on 2013-5-3

@author: sytmac
'''
import config
def ReadAdminInfo():
    with open('adminInfo.txt','wb') as fp:
        fp.writelines(config.admin_name+'\n')
        fp.writelines(config.admin_password)
