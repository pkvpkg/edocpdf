from django.shortcuts import render , HttpResponse,redirect
import pyodbc 
import os
import glob
from django.http import FileResponse, Http404
from ajworldapp import app_data
import pandas as pd

def index(request):
    return render(request,'index.html')
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    

def pdf(request):
    jobid = request.GET['jobid']
    cursor = app_data.conn.cursor()
    joib_first_four = jobid[0:4]
    cursor = app_data.conn.cursor()

    sql="select j.*,a.EI_DATE, a.[export/import] from JobShipmentEdoc as j left join [dbo].[Aj1] as a on a.JS_JobNumber = j.JSED_JobNumber where j.JSED_JobNumber = ? and j.JSED_DocType!='INV'  and ((j.JSED_DocType = 'HBL' and j.JSED_FileName like 'EMAIL%') or j.JSED_DocType ='DOR' or j.JSED_DocType ='MBL' or (j.JSED_DocType ='ARN'and j.JSED_FileName like '%SAJF%' or j.JSED_FileName like '%SLON%'))"

    daat_sql=cursor.execute(sql,jobid)
    data_list =[]
    for j in daat_sql:
        data_list.append(list(j))
    df = pd.DataFrame(data_list)
    
    if df.empty:
        return redirect('/empty_data')

    print(df)
    df[2] = df[2].str.replace('?','')
    
    df = df.drop_duplicates(subset=2,keep='last')

    header = ["S.No","File Name","Doc Saved Date","EI_Date","Download Link"]

    # cur_data=cursor.execute(sql,jobid)
    # df_data = pd.DataFrame(cur_data)

    files = glob.glob('ajworldapp/static/pdf_file/*')
    for fil in files:
        os.remove(fil)

    data_list = []
    
    file_data = []
    file_name = "File "
    count = 0
    for index,row in df.iterrows():
        count += 1
        print(row[2])
        file_detail = []
        value = row[3]
        
        with open("ajworldapp/static/pdf_file/"+row[2], "wb") as pdf:
            pdf.write(value)

        if not any(d['file_name'] == row[2] for d in file_detail):
            file_detail.append({"file_name":row[2]})
        else:
            pass

        doc_save_date = str(row[7])
        doc_save_date = str.split(doc_save_date)
        doc_save_date = doc_save_date[0]

        file_detail.append({"doc_save_date":doc_save_date})

        et_date = str(row[8])
        et_date = str.split(et_date)
        et_date = et_date[0]
        file_detail.append({"et_date":et_date})

        file_data.append(file_detail)
        print(file_detail)

        header = ["S.No","File Name","Doc Saved Date","EI_Date","Download Link"]

        if row[9]=="Export":
            header = ["S.No","File Name","Doc Saved Date","ETD_Date","Download Link"]
        elif row[9]=="Import":
            header = ["S.No","File Name","Doc Saved Date","ETA_Date","Download Link"]
        else:
            header = ["S.No","File Name","Doc Saved Date","EI_Date","Download Link"]

    return render(request,'pdf.html',{"header":header,"file_data":file_data})


def empty_data(request):
    return render(request,"empty_data.html")