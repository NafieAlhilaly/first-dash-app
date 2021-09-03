import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import base64
import io
import plotly.express as px
from scipy.stats import f_oneway, ttest_ind, ttest_rel
import random

data = pd.read_csv('assets/example_data.csv')
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
subject_info_table = pd.DataFrame(columns=['College', 'Department', 'Subject', 'Section', 'Year'])
summary_table_arr = pd.DataFrame(columns=['Parameter', 'values'])
summary_table_arr.Parameter = ["Mean",
                               "median",
                               "Mode",
                               "Std. Deviation",
                               "Skewness",
                               "Correlation",
                               "Maximum",
                               "Minimum",
                               "Total students"]


app.title = "Education measuring and evaluation system"
selected_sections = pd.DataFrame(columns=['sections'])

# modal for subjects and sections adding
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Add a course to analyze"),
                html.Div(className='row', children=[
                    html.Div(className='col-6',
                             children=[
                                 dbc.Input(id='course_name_input',
                                           placeholder="Course Name",
                                           style={'width': '200px', 'margin': '5px 20px auto 10px'}),
                                 dcc.Upload(
                                 id='upload-data',
                                 children=html.Div(['select sections']),
                                style={
                                    'width': '200px',
                                    'height': '50px',
                                    'lineHeight': '50px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': ' 5px 20px auto 10px',
                                },
                                # Allow multiple files to be uploaded
                                multiple=True),
                                 dbc.Button('clear',id='clear_course_btn', n_clicks=0)
             ]),
                    html.Div(id='uploaded_content', className='col-6 card')
                ]),
                dbc.ModalFooter([
                    dbc.Button('Add', id='add', className='btn btn-success', n_clicks=0),
                    html.Div(id='add_op_notify'),
                    dbc.Button(
                        "Close", id="close", className="ml-auto", n_clicks=0
                    )
                 ]),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Div(children="Courses", className="menu-title"),
                                                dcc.Dropdown(
                                                    options=[
                                                        {"label": course, "value": course}
                                                        for course in data.subject.unique()

                                                    ],
                                                    value="sub1",
                                                    id="subject",
                                                    clearable=False,
                                                    className="dropdown",
                                                    style={"width": "100%"}
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(children="sections", className="menu-title"),
                                                dcc.Dropdown(
                                                    id="section",
                                                    options=[
                                                        {"label": section, "value": section}
                                                        for section in selected_sections.sections.unique()

                                                    ],
                                                    value="All",
                                                    clearable=False,
                                                    searchable=False,
                                                    className="dropdown",
                                                ),
                                            ]
                                        ),
                                        html.Div(className="",children=[
                                            dbc.Button('+', id='add_sub',
                                                       className='btn_add align-item-end',n_clicks=0),
                                            modal
                                        ])
                                    ],
                                    className="card",
                                )
                                ,
                            html.Div(id="pie_div")
                            ],
                            className='col-lg-3 col-md-3 col-sm-12',
                            style={
                                'margin':' 10px auto 0px auto'
                            }
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        dash_table.DataTable(
                                            id='subject-info-table',
                                            columns=[
                                                {"name": i, "id": i} for i in subject_info_table.columns
                                            ],
                                            editable=True,
                                            style_header={
                                                'backgroundColor': '#E0E0E0',
                                                'fontWeight': 'bold'
                                            }
                                        ),
                                    ],
                                    className='container-fluid card col-12 '
                                ),
                                html.Div(id='bar_disc_table'
                                        ,children=[
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        children=[
                                                            dcc.Dropdown(
                                                                id="graph_selector",
                                                                options=[
                                                                    {"label": section, "value": section}
                                                                    for section in ['Bar graph',
                                                                                    'Scatter plot',
                                                                                    'Box plot',
                                                                                    'Line plot']
                                                                ],
                                                                value="Bar graph",
                                                                clearable=False,
                                                                searchable=False,
                                                                className="dropdown",
                                                            ),
                                                            dcc.Loading([
                                                            html.Div(id='graph_div')
                                                            ], type='circle')
                                                     ]
                                                     , className='card col-lg-8 col-md-12 col-sm-12')
                                                    ,
                                                    html.Div(className="card col-lg-4 col-md4 col-sm-12",children=[
                                                    html.Div(
                                                            children=[
                                                                html.P('Statistical Summary', className='p'),
                                                                html.P('معلومات احصائية وصفية', className='p'),
                                                                dcc.Loading([
                                                                    dash_table.DataTable(
                                                                        id='summary-table',
                                                                        columns=[{"name": i, "id": i} for i in
                                                                                 summary_table_arr.columns],
                                                                        style_header={
                                                                            'backgroundColor': '#E0E0E0',
                                                                            'fontWeight': 'bold'
                                                                        })
                                                                ],
                                                                type='circle'),
                                                                dcc.Loading([
                                                                    html.Div(id='hypo_test', className='')
                                                                ], type='circle')
                                                            ]
                                                        , className=''),
                                                    ]),
                                                ], className='row')

                                    ],
                                    className=' container'
                                ),
                            ],
                            className='col-lg-9 col-md-9 col-sm-12 align-item-start',
                            style={
                                'margin':'10px auto auto 0px'
                            }
                        ),

                    ]
                ,
                className='row')
            ],
            className="container-fluid"
        ),
    ]
)
def calcScoresDist(df):
    stds_a_count = df.total[df['total'] >= 90].count()
    stds_b_count = df.total[(df['total'] >= 80) & (df['total'] < 90)].count()
    stds_c_count = df.total[(df['total'] >= 70) & (df['total'] < 80)].count()
    stds_d_count = df.total[(df['total'] >= 60) & (df['total'] < 70)].count()
    stds_f_count = df.total[df['total'] < 60].count()

    return [stds_a_count,
            stds_b_count,
            stds_c_count,
            stds_d_count,
            stds_f_count]

def lstItems(lst_itm):
    return html.Li(lst_itm)

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df
        elif ('xls' in filename) or ('xlsx' in filename):
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df
    except Exception as e:
        print(e)

# uploading callback function
@app.callback(

    Output('add', 'n_clicks'),
    Output('course_name_input', 'value'),
    Output('course_name_input', 'placeholder'),
    Output('upload-data', 'contents'),
    Output('add_op_notify', 'children'),
    Output('uploaded_content', 'children'),
    Input('upload-data', 'contents'),
    Input('course_name_input', 'value'),
    Input('add', 'n_clicks'),
    State('upload-data', 'filename')
)

def showUploadedCont(list_of_contents, course_name, add_btn, list_of_names):
    global df
    df = pd.DataFrame()
    children = list()
    sec_lst = list()
    cors_lst = list()

    try:
        children = [
            html.P('Info of course to add :'),
            html.P('Course is ' + str(course_name)),
            html.P('sections files :'),
            html.Ul(children=[
                lstItems(i) for i in list_of_names
            ]),
        ]
    except TypeError as t:
        print()


    if add_btn:
        global data
        if list_of_contents is not None:
            for c, n in zip(list_of_contents, list_of_names):
                df = parse_contents(c, n)
                # getting text after '.' so we can remove extension
                ext = str(n).partition('.')[1] + str(n).partition('.')[2]
                sec_name = str(n).strip(ext)
                for i in range(len(df)):
                    sec_lst.append(sec_name)
                    cors_lst.append(str(course_name))
                df.insert(0, 'section', sec_lst)
                df.insert(0, 'subject', cors_lst)
                data = data.append(df, ignore_index=True)
                sec_lst.clear()
                cors_lst.clear()
            return 0, '', 'Course name', None,[html.P('Course added', style={'color': 'green'})], children
        elif list_of_contents is None:
            return 0, '', 'Course name', None, [html.P('please choose file/files first', style={'color': 'red'})], []

    return dash.no_update


@app.callback(
    Output('subject', 'options'),
    Input('add', 'n_clicks')
)

def update_subject_dropdown(clicks):
    try:
        global data
        subjects = list(data['subject'].unique())
        return [{'label': subject, 'value': subject} for subject in subjects]
    except:
        return dash.no_update

# callback to update sections based on selected subject
@app.callback(
    Output('section', 'options'),[
    Input('subject', 'value')]
)

def update_section_dropdown(subject):
    try:
        global data
        sections = list(data.section[data['subject'] == subject].unique())
        sections.append('All')
        return [{'label': section, 'value': section} for section in sections]
    except:
        return dash.no_update

# updating tables and graphs
@app.callback(
    Output('summary-table', 'data'),
    Output('graph_div','children'),
    Output('subject-info-table', 'data'),
    Input("subject", "value"),
    Input("section", "value"),
    Input('graph_selector', 'value')
)
def update_table(subject, section, graph):
    global data
    try:
        filtered_data = pd.DataFrame()

        if section != 'All':
            filtered_data = data[(data.subject == subject)
                                 & (data.section == section)]
        elif section == 'All':
            filtered_data = data[(data.subject == subject)]


        filtered_data = filtered_data.dropna()
        mean = round(filtered_data['total'].mean(), 3)
        median = filtered_data['total'].median()
        mode = filtered_data['total'].mode()
        std = round(filtered_data['total'].std(), 3)
        skewness = round(filtered_data['total'].skew(), 3)
        corr = round(filtered_data['mid'].corr(filtered_data['final']), 3)
        maximum = filtered_data['total'].max()
        minimum = filtered_data['total'].min()
        total_stds = len(filtered_data)

        rearranged_mode = ['['+str(i)+']' for i in mode]

        subject_info = subject_info_table.append(
            {"College": 'College of Computer Science',
             "Department": 'Department of Computer Science', "Subject": subject,
             "Section": section},
            ignore_index=True,
        )
        summary_table_arr['values'] = [mean,
                                       median,
                                       rearranged_mode,
                                       std,
                                       skewness,
                                       corr,
                                       maximum,
                                       minimum,
                                       total_stds]

        stds_dist = calcScoresDist(filtered_data)
        stds_rank = ['A count','B count', 'C count','D count','F count']

        if section == 'All':
            dist_df = pd.DataFrame()
            for i in filtered_data['section'].unique():
                dist_df.insert(0, str(i), calcScoresDist(filtered_data[filtered_data['section'] == i]))

            chart_figure = px.bar(dist_df, x=stds_rank, y=dist_df.columns, labels={'x':"Grades", 'y':'Frequency'})
            scatter_fig = px.scatter(filtered_data, x='mid', y='final', color='section',
                                     labels={'x': "Students mid scores", 'y': 'Students final scores'})
            box_fig = px.box(filtered_data, filtered_data['total'], color='section', orientation='h')

            # Scores normal distribution
            y = [2, 14, 68, 14, 2]
            x = [1, 2, 3, 4, 5]
            score_dist_df = pd.DataFrame()
            score_dist_df['X'] = x
            score_dist_df['Normal Distribution'] = y
            for i in filtered_data['section'].unique():
                stds_dist_percentage = [
                    ((calcScoresDist(filtered_data[filtered_data['section'] == str(i)])[0] / len(filtered_data[filtered_data['section'] == str(i)])) * 100),
                    ((calcScoresDist(filtered_data[filtered_data['section'] == str(i)])[1] / len(filtered_data[filtered_data['section'] == str(i)])) * 100),
                    ((calcScoresDist(filtered_data[filtered_data['section'] == str(i)])[2] / len(filtered_data[filtered_data['section'] == str(i)])) * 100),
                    ((calcScoresDist(filtered_data[filtered_data['section'] == str(i)])[3] / len(filtered_data[filtered_data['section'] == str(i)])) * 100),
                    ((calcScoresDist(filtered_data[filtered_data['section'] == str(i)])[4] / len(filtered_data[filtered_data['section'] == str(i)])) * 100)
                ]
                score_dist_df[str(i)] = stds_dist_percentage

            line_fig = px.line(score_dist_df, score_dist_df['X'], [*score_dist_df.columns],
                               labels={'x': '', 'value': ''},
                               line_shape='spline')

        else:
            chart_figure = px.bar(x=stds_rank, y=stds_dist, labels={'x': "Grades", 'y': 'Frequency'})
            scatter_fig = px.scatter(x=filtered_data['mid'], y=filtered_data['final'],
                                     labels={'x': "Students mid scores", 'y': 'Students final scores'})
            box_fig = px.box(filtered_data['total'], orientation='h')

            # Scores normal distribution
            y = [2, 14, 68, 14, 2]
            x = [1, 2, 3, 4, 5]

            stds_dist_percentage = [
                ((calcScoresDist(filtered_data)[0] / total_stds) * 100),
                ((calcScoresDist(filtered_data)[1] / total_stds) * 100),
                ((calcScoresDist(filtered_data)[2] / total_stds) * 100),
                ((calcScoresDist(filtered_data)[3] / total_stds) * 100),
                ((calcScoresDist(filtered_data)[4] / total_stds) * 100)
            ]

            score_dist_df = pd.DataFrame({'X': x,
                                          "Normal Distribution": y,
                                          "Student Distribution": stds_dist_percentage})
            line_fig = px.line(score_dist_df, score_dist_df['X'],
                               [score_dist_df['Normal Distribution'], score_dist_df['Student Distribution']],
                               labels={'x': '', 'value': ''},
                               line_shape='spline')



        if graph == "Bar graph":
            children = [
                html.P(
                    'Bar Graph shows students grades distribution and its count',
                    className='p'),
                html.P('رسمة توضح توزيع الطلاب على المعدلات وعددهم لكل معدل',
                       className='p'),
                dcc.Graph(figure=chart_figure, style={
                    'height':'420px'

                })
            ]
        elif graph == "Box plot":
            children = [
                 html.P(
                     'Box plot shows total scores range',
                     className='p'),
                 html.P('رسمة توظح مدى مجموع الدرجات',
                        className='p'),
                 dcc.Graph(figure=box_fig)]
        elif graph == "Scatter plot":
            children=[
                 html.P(
                     'Scatter graph show the correlation between mid scores and final exam scores',
                     className='p'),
                 html.P('رسمة توضح العلاقة بين درجات اعمال الفصل ودرجات الاختبار النهائي',
                        className='p'),
                 dcc.Graph(figure=scatter_fig)]
        elif graph == "Line plot":
            children=[
                 html.P(
                     'Graph show Students grades percentage distribution and normal distribution',
                     className='p'),
                 html.P('رسمة توضح توزيع معدلات الطلاب والمعدل الطبيعي ', className='p'),
                 dcc.Graph(figure=line_fig)]
        return summary_table_arr.to_dict('record'), children, subject_info.to_dict('record')
    except Exception :
        return dash.no_update
@app.callback(
    Output('hypo_test','children'),
    Input('section','value')
)

def createHypoTable(section):
    if section == 'All':
        hypo_table = pd.DataFrame(columns=['Test type', 'p-value'])
        hypo_table['Test type'] = ['T-test','One-way ANOVA']
        global data
        rnd_two_sections = random.sample(sorted(data['section'].unique()), k=2)
        all_sections = list()
        for i in data['section'].unique():
            sec = data.total[data['section'] == i]
            sec = sec.dropna()
            all_sections.append(sec)

        ttest_pval = ttest_ind(data.total[data['section'] == rnd_two_sections[0]],
                          data.total[data['section'] == rnd_two_sections[1]], equal_var=True, nan_policy='omit', )
        ttest_pval = f"{ttest_pval[1]:.11f}"

        anova_pval = f_oneway(*all_sections)
        anova_pval = f"{anova_pval[1]:.11f}"

        hypo_table['p-value'] = [ttest_pval,anova_pval]
        children = [
            html.P('Hypothesis testing table', className='p'),
            html.P('جدول اختبار الفرضيات الاحصائية', className='p'),
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in hypo_table.columns],
                data=hypo_table.to_dict('record'),
                style_header={
                    'backgroundColor': '#E0E0E0',
                    'fontWeight': 'bold'
                }
            )
        ]

        return children

@app.callback(
    Output("modal", "is_open"),
    Input("add_sub", "n_clicks"),
    Input('close','n_clicks'),
    State("modal", "is_open"),
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('pie_div','children'),
    Input('section','value'),
    Input('subject', 'value')
)

def creatPieChart(section, subject):
    count = pd.DataFrame()
    filtered_data = data[data['subject'] == subject]
    for c in filtered_data['section'].unique():
        count.insert(0, str(c), [len(filtered_data[filtered_data['section'] == str(c)])])
    clms = count.columns
    fig = px.pie(count, values=clms, names=clms, hole=.6)
    children=[
            html.P("Student count in every section"),
            html.P("عدد الطلاب في كل شعبة"),
            dcc.Graph(figure=fig)
        ]
    if section == 'All':
        return children

if __name__ == '__main__':
    app.run_server( debug=False)