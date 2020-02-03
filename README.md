Python3.6.6  Django1.11.5             
华东理工大学课程管理系统 2019.09.23 -- 2019.10.29    
保存目录：../course_arrangement

./start.sh -i 
       
用户组
超级用户组： Operator   有添加数据库记录权限、有浏览权限
普通用户组： Customer   无添加数据库记录权限，有浏览权限

### 一、系统管理员登录           
（一）登录系统         
http://localhost:8000/schedule/list/         

1、超级用户登录(有添加数据库记录权限、有浏览权限)                 
用户/密码 op0/1234qazx  (初始化创建)              
用户/密码 op1/1234qazx  (初始化创建)        

2、一般用户(无添加数据库记录权限，有浏览权限)           
用户/密码 cx0/1234qazx   (初始化创建)            
用户/密码 cx1/1234qazx   (初始化创建)          
  
（二）登录后台            
超级管理员  具有全部权限     
http://localhost:8000/admin/           
用户/密码  admin/1234qazx  (初始化创建)      

### 二、查询       
（一）课程查询、自习室查询查询       
http://localhost:8000/         

### 三、后台管理员(超级管理员, 具有全部权限)          
（一）校区 增、删、改 功能       
1、登录密码。用户/密码  admin/1234qazx      
2、登录网址。http://localhost:8000/admin/account/campusname/        

（二）教室 增、删、改 功能                  
1、登录密码。用户/密码  admin/1234qazx               
2、登录网址。http://localhost:8000/admin/account/classroom/              
            
（三）课表 增、删、改 功能            
1、登录密码。用户/密码  admin/1234qazx               
2、登录网址。http://localhost:8000/admin/account/schedule/               

（四）用户 增、删、改 功能              
1、登录密码。用户/密码  admin/1234qazx             
2、登录网址。http://localhost:8000/admin/auth/user/                  

### 四、超级用户功能                     
（一）批量导入课表                  
http://localhost:8000/schedule/import/                    
（二）批量导入教程             
http://localhost:8000/classromm/import/                    
（三）课表列表                  
http://localhost:8000/schedule/list/1                  
（四）教室列表                 
http://localhost:8000/romm/list/1              

```
测试效果            
http://localhost:8000/kcmc/details/        
奉贤校区 -- 实验二楼 -- 实验二楼101 -- 教室课程安排表      
2019-09-17 -- 星期2      

http://localhost:8000/self/study/list/       
 自习室查询 -- 徐汇校区 -- 研究生楼        
2019-09-14 -- 星期6        
```      
    