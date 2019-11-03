# -*- coding: UTF-8 -*-
import os
import sys
import django
import random
import datetime

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    from account.models import Classroom, Schedule

    
    #创建组operatorGroup
    operatorGroup = Group.objects.create(name='Operator')    
    operatorGroup.permissions.add(Permission.objects.get(name='Can add classroom'),\
                                  Permission.objects.get(name='Can add schedule')) 
    #创建组customerGroup
    customerGroup = Group.objects.create(name='Customer')   
    User.objects.create_superuser('admin', 'admin@test.com', '1234qazx')
     
    OPEERATOR_NUM = 2
    COMPANY_NUM = 2    
    for i in range(OPEERATOR_NUM):
        user = User.objects.create_user('op%s' % i, 'op%s@test.com' % i,
                                        '1234qazx')
        user.is_staff = True
        user.is_superuser = False
        user.groups.add(operatorGroup)
        user.save()      
          
    for i in range(COMPANY_NUM):
        user = User.objects.create_user('cx%s' % i, 'cx%s@test.com' % i,
                                        '1234qazx')
        user.is_staff = True
        user.is_superuser = False
        user.groups.add(customerGroup)
        user.save()   
    
    #校区 
    #mylist = ['奉贤校区','徐汇校区',] #'金山校区'
         
        
        