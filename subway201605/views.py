import django
from django.shortcuts import render
from django.http import HttpResponse

import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def compare_form(request):
    return render(request, 'subway201605/main.html',{})

def compare(request):
    data = csv.reader(open('201605subway.csv', 'r'), delimiter=",")
    역이름1,호선1,역이름2,호선2 = request.GET['station1'], request.GET['type1'], request.GET['station2'], request.GET['type2']
    # message = '비교대상: %s(%s) vs %s(%s)' % (request.GET['station1'],request.GET['type1'],request.GET['station2'],request.GET['type2'])
    인원1 = []
    인원2 = []
    승차1, 승차2, 하차1, 하차2 = [],[],[],[]
    for row in data:
        if (row[1] == 역이름1 and row[0] == 호선1):
            인원1 = row[2:]
        if (row[1] == 역이름2 and row[0] == 호선2):
            인원2 = row[2:]

    승차1 = 인원1[::2]
    하차1 = 인원1[1::2]
    승차2 = 인원2[::2]
    하차2 = 인원2[1::2]

    import matplotlib.pyplot as plt
    plt.rc('font', family='Malgun Gothic')

    labels = []
    x = []
    for i in range(4, 28):
        labels.append(str(i) + '시')
        x.append(i)
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation='vertical')
    ax.plot(x, 승차1, 'r', label=역이름1 + '역 승차')
    ax.plot(x, 승차2, 'b', label=역이름2 + '역 승차')
    ax.plot(x, 하차1, 'r--', label=역이름1 + '역 하차')
    ax.plot(x, 하차2, 'b--', label=역이름2 + '역 하차')
    ax.set_ylim(ymax=420000)
    ax.set_title(역이름1 + '역 승하차 인원 vs ' + 역이름2 + '역 승하차 인원   # 2016년 5월 티머니카드 제공 데이터')
    ax.legend()

    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def simple(request):
    data = csv.reader(open('201605subway.csv', 'r'), delimiter=",")

    max_person1 = [0] * 24
    max_station1 = [''] * 24

    max_person2 = [0] * 24
    max_station2 = [''] * 24
    for row in data:
        for i in range(24):
            if int(max_person1[i]) < int(row[2 + (i * 2)]):
                max_person1[i] = row[2 + (i * 2)]
                max_station1[i] = row[1] + '/' + str(i + 4)  # +'('+ row[0]+')'
            if int(max_person2[i]) < int(row[3 + (i * 2)]):
                max_person2[i] = row[3 + (i * 2)]
                max_station2[i] = row[1] + '/' + str(i + 4)  # +'('+ row[0]+')'

    fig = plt.figure(figsize=(20, 8))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    plt.rc('font', family='Malgun Gothic')
    cnt = np.arange(24)
    ax1.set_title('2016년 5월 서울시 지하철 시간대별 최다 승차역')
    ax1.plot(cnt, max_person1, 'r')
    ax1.set_xticks(cnt)
    ax1.set_xticklabels(max_station1, rotation = 45, fontsize = 9)
    ax1.set_ylim(ymax=450000)
    ax2.set_title('2016년 5월 서울시 지하철 시간대별 최다 하차역')
    ax2.plot(cnt, max_person2, 'b')
    ax2.set_xticks(cnt)
    ax2.set_xticklabels(max_station2, rotation = 45, fontsize = 9)
    ax2.set_ylim(ymax=450000)

    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response