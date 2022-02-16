from django.contrib import messages
import os.path
from django.shortcuts import render,redirect
from csvproject.settings import CSV_FILE
from .models import Data, File
from .forms import FileForm
import pandas as pd
import csv

# Function to upload and validate file data
def upload_file(request):
    if request.method == 'POST':
        files = request.FILES['csv_file'] or None
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            savedata(request,files)
            return redirect('index')
        else:
            return render(request, 'index.html',{'form':form})
    form = FileForm()
    return render(request, 'index.html',{'form':form})


# Function to store file data into db
def savedata(request,files):
    obj = File.objects.get(csv_file=files.name) or None
    if obj:
        df = pd.read_csv(obj.csv_file.path)
        img = df['image_name']
        obj = df['objects_detected']
        ts= df['timestamp']
        iter = len(df)
        for i in range(iter):
            Data.objects.create(
                image_name = img[i], 
                objects_detected = obj[i], 
                timestamp = ts[i]
                )
        messages.success(request,'Data saved!')
    else:
        messages.error(request,'Error! Data not saved!')


# Function to retreive data between two dates
def getData(request):
    if request.method == 'POST':
        form = FileForm()
        from_date = request.POST['from']
        to_date = request.POST['to']
        if from_date and to_date:
            data = Data.objects.filter(timestamp__range=[from_date, to_date])
            if data:
                str_data = CountStrings(data)
                ToCSV(str_data)
                messages.success(request, 'Data fetched and record generated!!')
                return render(request,'index.html',{'data':data,'form':form})
            else:
                messages.error(request, 'No Records!!')
                redirect('index')
        else:
            messages.error(request,'Select appropriate date')
        form = FileForm()
        data = None
        return render(request,'index.html',{'data':data,'form':form})
    return render(request,'index.html',{})


# Function to count number detected_objects in db
def CountStrings(data):
    data_count = []
    list_data = []
    data_values = list(data.values())
    for i in range(len(data)):
        temp_data = data_values[i]['objects_detected'].split(',')
        list_data.append(temp_data)
    str_data = ['jewellery','watch','gun','mobile','knife','e-cigarette','scissor','nail_cutter','cigar_cutter','laptop','lighter',
    'battrey','ammo','gold','plier','cigarette_case','cigarette','cigar']
    for i in range(len(str_data)):
        count = 0
        for j in range(len(list_data)):
            for k in range(len(list_data[j])):
                if str_data[i] == list_data[j][k]:
                    count = count + 1
        data_count.append(count)
    context = {
        'str_data' : str_data,
        'data_count' : data_count
    }
    return context


# Function to deploy calculated specific data to .csv file 
def ToCSV(context):
    csv_columns = ['Threat', 'Occurance']
    dicts_data = {}
    dicts = []
    for i in range(len(context['str_data'])):
        dicts_data['Threat'] = context['str_data'][i]
        dicts_data['Occurance'] = context['data_count'][i]
        dicts.append(dicts_data.copy())
    csv_file = os.path.join(CSV_FILE,"data.csv")
    if os.path.isfile('data.csv'):
        os.remove('data.csv')
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dicts:
                writer.writerow(data)
    except IOError:
        print("I/O error")
