#!/usr/bin/python3
import requests
import pandas as pd
import plotly.express as px

# res = requests.get('https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D03001-001&l=https://data.nhi.gov.tw/resource/Nhi_Fst/Fstdata.csv')
# with open ('Fstdata.csv','wb')as f:
#     f.write(res.content)

df = pd.read_csv('https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D03001-001&l=https://data.nhi.gov.tw/resource/Nhi_Fst/Fstdata.csv')
data = []
cityslist = []
towns = []
for a,b,c in zip(df['醫事機構名稱'],df['醫事機構地址'],df['快篩試劑截至目前結餘存貨數量']):
    data.append([a,b[:3],b[3:6],c])
    cityslist.append(b[:3])
    towns.append(b[3:6])

citys = list(set(cityslist))
df1 = pd.DataFrame(data,columns=['name','city','town','value'])
#設定圖表 排序value
fig = px.bar(x=df1['name'],y=df1['value'].sort_values(ascending=False),color=df1['city'],title='↓《快篩試劑全省藥局分布》請選擇縣市')
#排序集合
citys.sort(key=cityslist.index)


def dict_bar(citys):
    resultlist = []
    for i in range(len(citys)):
        faslelist = [False for i in range(len(citys))]
        faslelist[i]=True

        result = dict(label=citys[i],
             method="update",
            #控制True & False 位置
             args =[ {"visible":faslelist},
                     {'showlegend': True}
                     ])
        resultlist.append(result)
    return resultlist

fig.update_layout(
    updatemenus=[
        dict(
            # type="buttons" 取消才有下拉式選單,
            #下拉式選單呈現往下選擇
            direction="down",
            active=0,
            buttons=list([i for i in dict_bar(citys)
            ]),
        )
    ]
)
fig.write_html('index.html')
