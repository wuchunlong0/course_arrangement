# -*- coding: utf-8 -*-
import os,datetime,xlrd
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from django.contrib.auth.decorators import login_required

from .models import Classroom, Schedule
from myAPI.pageAPI import djangoPage,PAGE_NUM,toInt
from myAPI.dateAPI import get_year_weekday, get_weekday, get_date

def _getOperators():
    operators = Group.objects.get(name='Operator').user_set.all()
    return [user for user in User.objects.all() if user.is_superuser or user in operators]

def get_year_whichweek_week(date_str):
    """ 例如：date_str='2019-09-02' 2019秋季开学第一学期，初始化值('2020-1')     
        返回数据含意               ('2019秋季开学第一学期', 相对开学第几周(开学是第1周), 星期几, 1或2)    
        date_str = '2019-09-02'    返回 '2020-1' 1 1 1          
        date_str = '2019-09-25'    返回 '2020-1' 4 3 2
                        
        数据格式含意：
        1、2019-2020-1：2019秋季开学第一学期；
        2、开学时间（学校规定）：2019-09-02；
        3、数据库字段SJBZ：只有0、1、2三个数字，0代表每周都有课，1代表单数周有课，2代表双数周有课        
    """    
    if '2019-09' in date_str: 
        date_str0 = '2019-09-02' #2019-09-02开学
    else: return '',0,0,0  
    s0 = get_year_weekday(date_str0)    
    s1 = get_year_weekday(date_str)
    if s0[0] != s1[0]: return '',0,0,0
    w = s1[1] - s0[1] + 1 #相对开学第几周
    sjbz=2 if w%2 == 0 else 1 #sjbz:1代表单数周有课，2代表双数周有课
    return '%s-1'%(s0[0]+1), w, s1[2], sjbz 

def get_update_downdate(cleanData):
    """ 今天 上一天 下一天
        返回 类似这样：2019-09-28,0    
    """
    todaydate = cleanData.get('todaydate','')
    date = cleanData.get('date','')
    update = cleanData.get('update','')
    downdate = cleanData.get('downdate','')
    count = cleanData.get('count','')
    count = int(count) if count else 0              
    if todaydate:  count = 0 #今天       
    if update:  count -=  1 #上一天            
    if downdate: count += 1 #下一天   
    data_str = date if date else get_date(count)    
    return data_str,count
        
def test(request):
    date_str = '2019-09-02'
    return HttpResponse(get_year_whichweek_week(date_str))

def post_excel_model(request, post_file_excel, model, k):
    ''' Excel文件，多张工作表（数据），导入到数据库
        post_file_excel: 前端上传的文件名
        model:  数据库
        K: 数据库字段, 与Excel表格列对应    
    '''
    file_excel = request.FILES.get(post_file_excel)
    ext = os.path.splitext(file_excel.name)[1]    
    if 'xls' not in ext and 'xlsx' not in ext:
        return 'err: 文件格式错误，请上传Excel文件。'         
    model.objects.all().delete() #删除数据库     
    workbook = xlrd.open_workbook(file_contents=file_excel.file.read())
    sheet_sum = len(workbook.sheet_names())  # 获取电子表格 工作表总数
    for index in range(0, sheet_sum):
        ret = workbook_model(workbook, 0, index, model, k) #从电子表格0行开始
        if ret[0:3] == 'err':
            return ret
    return str(sheet_sum)

def workbook_model(workbook, x, index, model, k):
    """ 电子表格，多张工作表写入数据库
        workbook: workbook = xlrd.open_workbook(file_contents=file_excel.file.read())
        x: 从x行开始  x=0,1,2...
        index: 工作表序号
        model: 数据库
        K: 数据库字段, 与Excel表格列对应         
    """
    sheet = workbook.sheet_by_index(index)  
    try:
        #1.1、电子表格转换为列表
        mylist = []
        for row_num in range(x, sheet.nrows): #从x行开始  x=0,1,2...
            row = sheet.row(row_num) #row -- [empty:'', empty:'', text:'HZ-616S', number:10000.0]           
            v = []
            for (n,r) in enumerate(row): #一次处理电子表格一行
                if n == 10 or n == 11 or n == 12 or n == 13 or n == 14:
                    if r.value:                    
                        v.append(int(r.value))                        
                    else:
                        v.append(0)                              
                else:
                    v.append(r.value)
            mylist.append(v)
                                 
        #2.1、数据写入数据库 
        object_list = []      
        for v in mylist:
            d = dict(zip(k,v)) 
            object_list.append(model(**d))                 
        model.objects.bulk_create(object_list, batch_size=20)
        return 'ok'
    except Exception as e:
        print(e)
        return 'err: %s. 错误工作表：%s'%(e, index+1)

@login_required
def classromm_import(request):
    """批量导入 课程进度表"""
    operators = _getOperators()
    if request.method == 'GET':
        return render(request, 'account/import.html',context=locals())
    
    k = ['ROOM_ID','ROOM_NAME','BUILDING','TYPE','CAMPUS']    
    ret = post_excel_model(request, 'post_file_excel', Classroom, k) 
    contxt = {'status': False, 'msg': '导入失败! %s' %ret} if ret[0:3] == 'err' \
        else  {'status': True, 'msg': '导入成功! 导入了%s张工作表. ' %ret}     
    return render(request, 'account/import.html',context=locals())

@login_required
def schedule_import(request):
    """批量导入 课程进度表"""
    operators = _getOperators()
    if request.method == 'GET':
        return render(request, 'account/import.html',context=locals())
    
    k = ['JX0404ID','TERMNAME','KCMC','TEACHER_ID',
        'TEACHER_NAME','CLASS_TIME','START_TIME','CLASSROOM_NAME',\
        'CLASSROOM_ID','XQ','KS','JS','ZC1','ZC2','SJBZ','SHOWTEXT']    
    ret = post_excel_model(request, 'post_file_excel', Schedule, k) 
    contxt = {'status': False, 'msg': '导入失败! %s' %ret} if ret[0:3] == 'err' \
        else  {'status': True, 'msg': '导入成功! 导入了%s张工作表. ' %ret}     
    return render(request, 'account/import.html',context=locals())

#教室列表
@login_required
def romm_list(request, page):
    operators = _getOperators()
    cleanData = request.GET.dict() 
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()]) 
    datas = Classroom.objects.filter()
    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  
    offset = PAGE_NUM * (page - 1) 
    return render(request, 'account/classromm_list.html', context=locals())

#课程列表
@login_required
def schedule_list(request, page):
    operators = _getOperators()
    cleanData = request.GET.dict() 
    queryString = '?'+'&'.join(['%s=%s' % (k,v) for k,v in cleanData.items()]) 
    datas = Schedule.objects.filter()
    data_list, pageList, num_pages, page = djangoPage(datas,page,PAGE_NUM)  
    offset = PAGE_NUM * (page - 1) 
    return render(request, 'account/schedule_list.html', context=locals())

@login_required
def classromm_list(request):
    operators = _getOperators()
    cleanData = request.GET.dict()
    data_list = Classroom.objects.filter(ROOM_ID = cleanData['room_id'])[:1]
    return render(request, 'account/classromm_list.html', context=locals())

#课程列表
@login_required
def schedule_filter(request):
    operators = _getOperators()
    cleanData = request.GET.dict()                    
    if request.method == 'POST':
        cleanData = request.POST.dict()
    
    models = Schedule.objects 
    data_str,count = get_update_downdate(cleanData)
    kcmc = cleanData.get('kcmc', '')
    if kcmc: 
        models = models.filter(KCMC__icontains = kcmc) 

    TEACHER_NAME = cleanData.get('TEACHER_NAME', '')
    if TEACHER_NAME: 
        models = models.filter(TEACHER_NAME__icontains = TEACHER_NAME) 

    CLASSROOM_NAME = cleanData.get('CLASSROOM_NAME', '')
    if CLASSROOM_NAME: 
        models = models.filter(CLASSROOM_NAME__icontains = CLASSROOM_NAME) 
               
    date = cleanData.get('date', '')
    data_list = _filter_model(models, date) if date else _filter_model(models, data_str)      
    weekday = get_weekday(data_str)      
    return render(request, 'account/schedule_filter.html', context=locals())

def _filter_model(models, date_str):
    """ 按时间过滤
        models： 数据库记录
        date_str： 时间字符串 '2019-09-29'
        返回过滤后的数据库记录
    """
    model = ''    
    TERMNAME,whichweek,week, sjbz = get_year_whichweek_week(date_str)
    if TERMNAME:
        model = models.filter(TERMNAME__icontains = TERMNAME,\
                ZC1__lte = whichweek, ZC2__gte = whichweek,\
                XQ__icontains = str(week), SJBZ = sjbz).order_by("-id")|\
                models.filter(TERMNAME__icontains = TERMNAME, \
                ZC1__lte = whichweek,ZC2__gte = whichweek,\
                XQ__icontains = str(week), SJBZ = 0).order_by("-id")
    return  model


#课程查询、自习室查询 查询 
@login_required
def query_list(request):
    operators = _getOperators()
    querys = ['课程查询','自习室查询']
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query == querys[0]:
            return HttpResponseRedirect('/building/list/?query=%s' %query)
        if query == querys[1]:
            return HttpResponseRedirect('/self/building/list/?query=%s' %query)
    return render(request, 'account/query_list.html', context=locals()) 

#课程查询   
#校区 -- 教学楼列表
def building_list(request):
    operators = _getOperators()
    cleanData = request.GET.dict()
    campus_list = list(set(Classroom.objects.values_list('CAMPUS', flat=True))) #校区列表    
    if request.method == 'POST':     
        cleanData = request.POST.dict()
        for campus in campus_list:
            if campus == cleanData.get('campus',''):
                buildings = list(set(Classroom.objects.filter(\
                    CAMPUS=campus).values_list('BUILDING', flat=True))) #教学楼列表 
                return render(request, 'account/building_list.html', context=locals())        
    return render(request, 'account/campus_list.html', context=locals())


#教学楼 -- 教室列表
def room_list(request):
    operators = _getOperators()
    if request.method == 'POST':
        cleanData = request.POST.dict()
        rooms = list(set(Classroom.objects.filter(BUILDING =\
            cleanData.get('building','')).values_list('ROOM_NAME', flat=True))) #教室列表         
    return render(request, 'account/room_list.html', context=locals())    
        


#教室、时间 -- 教室课程表
def kcmc_details(request):  
    operators = _getOperators()
    cleanData = request.GET.dict()            
    if request.method == 'POST':
        cleanData = request.POST.dict() 

    data_str,count = get_update_downdate(cleanData) # 2019-09-28,0  
          
    query,campus,building,room = cleanData.get('query',''),cleanData.get('campus',''),\
            cleanData.get('building',''),cleanData.get('room','')              
         
    weekday = get_weekday(data_str)       
    models = Schedule.objects.filter(CLASSROOM_NAME__icontains = \
            cleanData.get('room', '')) #由教室名 获得记录   信息楼109A
    data_list =  _filter_model(models, data_str) 

    mylist = []
    for n in range(0,12):
        mylist.append(['','','',''])
    
    for model in data_list:  
        ks = model.KS
        js = model.JS              
        for n in range(ks-1,js):
            mylist[n] = [model.START_TIME, model.KCMC, model.TEACHER_NAME,model.CLASSROOM_ID]
    
    mlist = []
    k = ['j','START_TIME','KCMC','TEACHER_NAME','CLASSROOM_ID']
    for (index,m) in enumerate(mylist):
        v = ['第%s节'%(index+1), m[0], m[1], m[2], m[3]]
        d = dict(zip(k,v))
        mlist.append(d)
    return render(request, 'account/kcmc_details_list.html', context=locals())

def course_list(request):
    operators = _getOperators()
    cleanData = request.GET.dict()
    date_str = cleanData.get('date','')
    cid = cleanData.get('cid','')
    
    weekday = get_weekday(date_str) 
    models = Schedule.objects.filter(KCMC = cleanData.get('kcmc',''),\
                        TEACHER_NAME = cleanData.get('t',''))
    data_list = _filter_model(models, date_str)
    campus = Classroom.objects.filter(ROOM_ID=cid).first().CAMPUS

    building = Classroom.objects.filter(ROOM_ID=cid).first().BUILDING
    room = Classroom.objects.filter(ROOM_ID=cid).first().ROOM_NAME
    return render(request, 'account/course_details_list.html', context=locals())


#自习室查询
#校区 -- 教学楼列表
def self_building_list(request):
    operators = _getOperators()
    query = request.GET.get('query', '')
    campus = list(set(Classroom.objects.values_list('CAMPUS', flat=True)))#校区列表 
    if request.method == 'POST':     
        cleanData = request.POST.dict()
        query = cleanData.get('query', '') #查询
        campus = cleanData.get('campus','') #校区
        buildings = list(set(Classroom.objects.filter(\
                    CAMPUS=campus).values_list('BUILDING', flat=True))) #教学楼列表 
        return render(request, 'account/self_building_list.html', context=locals())        
    return render(request, 'account/self_campus_list.html', context=locals())


# 自习教室查询
def self_study_list(request):
    """1、自习教室是 教室类型为多媒体教室，并且课程为空的课节
       
    """
    operators = _getOperators()
    cleanData = request.GET.dict()  
    if request.method == 'POST':
        cleanData = request.POST.dict()
        
    data_str,count = get_update_downdate(cleanData) # 2019-09-28,0  
          
    query,campus,building,room = cleanData.get('query',''),cleanData.get('campus',''),\
            cleanData.get('building',''),cleanData.get('room','') #查询 校区 教学楼名称               
                        
    weekday = get_weekday(data_str) 
              
    #获得 教室类型为多媒体教室的id 
    room_ids = list(set(Classroom.objects.filter(TYPE__icontains = \
            '多媒体教室', CAMPUS__icontains = campus,\
            BUILDING__icontains = building).values_list('ROOM_ID', flat=True)))

    models = Schedule.objects.filter(CLASSROOM_ID='xxxx') #空记录   
    for room_id in room_ids:
        models = models|Schedule.objects.filter(CLASSROOM_ID=room_id)
                             
    data_list = []
    datas = _filter_model(models, data_str) #data_str时间过滤     
    if datas:                        
        #获得教室名列表
        classroom_names = list(set(datas.filter().values_list('CLASSROOM_NAME', flat=True)))
        for classroom_name in classroom_names:
            model_list = datas.filter(CLASSROOM_NAME__icontains=classroom_name)   
            mlist = ['','','','','','','','','','','','']
               
            for model in model_list:  
                ks = model.KS
                js = model.JS              
                for n in range(ks-1,js):
                    mlist[n] = (n+1)
         
            if any(mlist):
                mlist.insert(0, classroom_name) #插入             
                data_list.append(mlist)   
    return render(request, 'account/self_study_list.html', context=locals()) 
   
