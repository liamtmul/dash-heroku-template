import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

markdown_text = '''
The first article that I found: [How to close the gender pay gap: solutions from Sheryl Sandberg, Kathy Matsui and more](https://www.ft.com/content/29a02913-920e-4332-b230-529f31221513) (Financial Times). This article discusses what is behind the gender pay gap and how to close the divide. Sheryl Sandberg the COO of Facebooks originially believed the issue was that women do not ask for more money. The data did not support this hypothesis and Sandberng now believes
that this is atributed to gender norms and perceptions. Women are expected ot take a communal approach an not advocate too much for themselves. Sandberg says that women need to reposition their ask to explain how giving them a raise will help the entire team. 

She also thinks that the #MeToo movement has hampered the effort  close this gap because it has made manager more cautious around female employees. 

Another women interviewed, Tracey Chou, is a software engineer. She believes the issue is a lack of diversity in the venture capital community. 

Other solutions involve increasing paternity leave and providing tax incentives to companies who publish their salary information.

The second article that I found: [The gender pay gap no-one talks about](https://www.bbc.com/worklife/article/20200806-the-gender-pay-gap-no-one-talks-about) (BBC). This article disccusses the gap in stock-options given to employees. They found that the differences between men and women were 15-30%.Most of this difference comes from retention and not from potential. The authors main point is that stock options are substantial and companies need too look at this difference as well as base pay.

'''

avg_by_sex=gss_clean[['sex','income','job_prestige','socioeconomic_index','education']].groupby(gss_clean['sex']).agg('mean')
avg_by_sex=round(avg_by_sex,2)
avg_by_sex=avg_by_sex.reset_index().rename({'sex':'Sex', 'income':'Avg. Inc.', 'job_prestige': 'Avg. Occup. Prestige', 'socioeconomic_index':'Avg. Socioeconomic Ind', 'education': 'Avg. Years of Edu'}, axis=1)
table = ff.create_table(avg_by_sex)

bread_win_by_sex=gss_clean[['sex','male_breadwinner']]

bread_win_by_sex['male_breadwinner']=bread_win_by_sex['male_breadwinner'].astype('category')

bread_win_by_sex=bread_win_by_sex.groupby(['sex','male_breadwinner']).size().reset_index()

bread_win_by_sex=bread_win_by_sex.rename({0:'count'}, axis=1)

bread_win_by_sex['text'] = bread_win_by_sex['count'].astype(str)

fig3 = px.bar(bread_win_by_sex, x='male_breadwinner', y='count', color='sex',
            labels={'male_breadwinner':'Men should be the breadwinner?', 'count':'Number'},
            hover_data = ['sex', 'male_breadwinner', 'count'],
            text='text')
fig3.update_layout(showlegend=False)
fig3.update(layout=dict(title=dict(x=0.5)))


job_vs_income=gss_clean[['job_prestige','income','sex','education','socioeconomic_index']]


fig4 = px.scatter(job_vs_income, x='job_prestige', y='income',
                 trendline="ols",
                 color = 'sex', 
                 height=600, width=600,
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig4.update(layout=dict(title=dict(x=0.5)))

fig5 = px.box(job_vs_income, x='income', y = 'sex', color = 'sex',
                   labels={'income':'income', 'sex':''})
fig5.update(layout=dict(title=dict(x=0.5)))

fig5b = px.box(job_vs_income, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Job Prestige', 'sex':''})
fig5b.update(layout=dict(title=dict(x=0.5)))

inc_sex_job=gss_clean[['income','sex','job_prestige']]

inc_sex_job=inc_sex_job.dropna(how='any')

names = ['low prestige',' low medium prestige','medium prestige','high medium prestige','high prestige', 'very high prestige']

inc_sex_job['job_prestige_rating'] = pd.cut(inc_sex_job['job_prestige'], bins=6, labels=names)

fig6 = px.box(inc_sex_job, x='sex', y='income',color='sex', 
                 facet_col='job_prestige_rating', facet_col_wrap=2,
                 hover_data=['income','sex','job_prestige'],
                 color_discrete_map = {'male':'blue', 'female':'red'},
                 labels={'income':'Annual Income', 
                        'job_prestige':'Job Prestige'},
                 title = 'Job Prestige vs Income based on Gender',
                 width=1000, height=400)
fig6.update(layout=dict(title=dict(x=0.5)))
fig6.update_layout(showlegend=False)
fig6.for_each_annotation(lambda a: a.update(text=a.text.replace("sex=", "")))

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(
    [
        html.H1("Exploring the differences in Income and Job Prestige between Men and Women"),
        
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Mean income, occupational prestige, socioeconomic index, and years of education for men and for women"),
        
        dcc.Graph(figure=table),
        
        html.H2("Opinions on Male Breadwinner"),
        
        dcc.Graph(figure=fig3),
        
        html.H2("Job Prestige vs. Income"),
        
        dcc.Graph(figure=fig4),
        
        html.H2("Distribution of Income and Job Prestige"),
        
        dcc.Graph(figure=fig5),
        
        dcc.Graph(figure=fig5b),
        
        html.H2("Income Distributions within Job Prestige Categories"),
        dcc.Graph(figure=fig6)
    ]
)

if __name__ == '__main__':
    #app.run_server( debug=True)
    app.run_server(mode='inline', debug=True, port=591)
if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')
