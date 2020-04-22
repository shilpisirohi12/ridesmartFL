from flask import Flask,render_template,request,redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import json
import requests

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

"""Setting up the app"""
app=Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.secret_key='cutr_usf'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://cutr:cutr@127.0.0.1:3306/cutr'

engine=create_engine('mysql://cutr:cutr@127.0.0.1:3306/cutr')
#conn=engine.connect()
db=SQLAlchemy(app)
URL='http://127.0.0.1:5000'


""" Mapping Database Table """
class fatalities(db.Model):
    __tablename__ = 'fatalities'
    crsh_num=db.Column('CRSH_NUM',db.Unicode, primary_key=True)
    year=db.Column('CAL_YR',db.Unicode)
    dist_code=db.Column('MANDIST',db.Unicode)
    county_code=db.Column('CONTYDOT',db.Unicode)
    event_crash_date=db.Column('EVNT_CRSH_DT',db.Unicode)
    body_type=db.Column('VHCL_BDY_TYP_CD',db.Unicode)
    dr_inj_severity=db.column('DR_INJSEVER',db.Unicode)
    p1_inj_severity=db.column('P1_INJSEVER',db.Unicode)

    def __repr__(self):
        return self.crsh_num    


#filters values
year=['2011','2012','2013','2014','2015','2016','2017','2018']
district=['1','2','3','4','5','6','7']
countyName=['Charlotte','Citrus','Collier','Desoto','Glades','Hardee','Hendry','Hernando','Highlands','Hillsborough','Lake','Lee','Manatee','Pasco','Pinellas','Polk','Sarasota','Sumter','Alachua','Baker','Bradford','Columbia','Dixie','Gilchrist','Hamilton','Lafayette','Levy','Madison','Marion','Suwannee','Taylor','Union','Bay','Calhoun','Escambia','Franklin','Gadsden','Gulf','Holmes','Jackson','Jefferson','Leon','Liberty','Okaloosa','Santa Rosa','Wakulla','Walton','Washington','Brevard','Clay','Duval','Flagler','Nassau','Orange','Putnam','Seminole','St Johns','Volusia','Broward','Miami-Dade','Indian River','Martin','Monroe','Okeechobee','Osceola','Palm Beach','St Lucie']



"""Starting point of the Dashboard app"""
@app.route('/dashboard', methods=['GET','POST'], endpoint='start')
def start():
    """Below code is for graphs which shows the Motorcycle created data for florida"""

    query="SELECT CAL_YR as year,COUNT(*) as cnt  FROM FATALITIES WHERE "
    queryTraffic="SELECT CAL_YR as year,COUNT(*) as cnt  FROM FATALITIES WHERE "
    params={}
    paramsTraffic={}
    #URL for graph# 1 ( MC fatalities in florida)
    requestURL=URL+'/api/v1/resources/getFatalities'
    requestURLFatal=URL+'/api/v1/resources/getTrafficFatalities'

    #URL for graph# 3 Seriously Injured Motorcyclists by Month (2016-2018 Average)
    requestURLInjuredAverage=URL+'/api/v1/resources/getInjuredOperators'

    #URL for graph# 4 fatal Motorcyclists by Month (2016-2018 Average)
    requestURLfatalAverage=URL+'/api/v1/resources/getFatlMCOperators'

    print(requestURL)
    if request.method=='POST':
        year_selected=request.form.get('year')
        dist_selected=request.form.get('district')
        county_selected=request.form.get('county')

        """Setting values for parameters"""
        if int(year_selected) > 0:
            params['year']=year_selected
            #paramsTraffic['year']=year_selected
        if int(dist_selected) > 0:
            params['district']=dist_selected
            #paramsTraffic['district']=dist_selected
        if int(county_selected) > 0:
            params['county']=county_selected
            #paramsTraffic['county']=county_selected
        if int(year_selected)==0 and int(dist_selected)==0 and int(county_selected)==0:
            params['query']='all'
            #paramsTraffic['query']='all'
    else:
        params['query']='all'
        #paramsTraffic['queryTraffic']='all'

        
    res=requests.get(requestURL,params=params)  
    trafficFatal=requests.get(requestURLFatal,params=params)
    injuredAverage=requests.get(requestURLInjuredAverage,params=params) 
    fatalAverage=requests.get(requestURLfatalAverage,params=params)

    # print("res----->")
    # print(res)
    # print("\n\n trafficFatal----->")
    # print(trafficFatal)
    # print("\n\n injuredAverage----->")
    # print(injuredAverage)   
    # print("\n\n fatalAverage----->")
    # print(fatalAverage)    

    #Calculating Proportions
    proportions_fatal=[]
    for data,traffic in zip(json.loads(res.text),json.loads(trafficFatal.text)):
        proportions_fatal.append({'year':data['year'],'fatalities':round(float(data['fatalities']/traffic['fatalities']*100),2)})
    # print(proportions_fatal)
    
    return render_template('dashboard.html',mc_data=json.loads(res.text),traffic=json.loads(trafficFatal.text),proportions=proportions_fatal,injuredAverage=json.loads(injuredAverage.text),fatalAverage=json.loads(fatalAverage.text), years=year,districts=district,counties=countyName)

# @app.route("/",endpoint='homepage')
# def homepage():
#     render_template('index.html')

"""API to query database to get motorcycle fatalities"""
@app.route("/api/v1/resources/getFatalities", methods=['GET'], endpoint='getFatalities')
def getFatalities():
    data=[]
    query=db.session.query(fatalities.year, db.func.count(fatalities.crsh_num).label('total')).filter(fatalities.dr_inj_severity=='5').filter(fatalities.body_type=='11').order_by(fatalities.year)
    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            fatality_result=query.group_by(fatalities.year).all()
    else:        
        if 'year' in request.args:
            yr=request.args['year']
            yrList=yr.split(",")
            query=query.filter(fatalities.year.in_(yrList))
        if 'county' in request.args:
            county=request.args['county']
            query=query.filter(fatalities.county_code==county)
        if 'district' in request.args:
            district=request.args['district']
            query=query.filter(fatalities.dist_code==district)
        fatality_result=query.group_by(fatalities.year).all()
    for res in fatality_result:
        #print(res)
        data.append({'year':res.year,'fatalities':res.total})
    resp= app.response_class(
        response=json.dumps(data),
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

"""API to query database to get traffic fatalities"""
@app.route("/api/v1/resources/getTrafficFatalities", methods=['GET'], endpoint='getTrafficFatalities')
def getTrafficFatalities():
    data=[]
    query=db.session.query(fatalities.year, db.func.count(fatalities.crsh_num).label('total')).filter(fatalities.dr_inj_severity=='4').order_by(fatalities.year)
    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            fatality_result=query.group_by(fatalities.year).all()
    else:        
        if 'year' in request.args:
            yr=request.args['year']
            yrList=yr.split(",")
            query=query.filter(fatalities.year.in_(yrList))
        if 'county' in request.args:
            county=request.args['county']
            query=query.filter(fatalities.county_code==county)
        if 'district' in request.args:
            district=request.args['district']
            query=query.filter(fatalities.dist_code==district)
        #print("query------------>")
        #print(query)
        fatality_result=query.group_by(fatalities.year).all()
    #print(request.args)
    for res in fatality_result:
        #print(res)
        data.append({'year':res.year,'fatalities':res.total})
    resp= app.response_class(
        response=json.dumps(data),
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp    


"""API to query database to get Fatal MC Operators"""
@app.route("/api/v1/resources/getFatlMCOperators", methods=['GET'], endpoint='getFatalMCOperators')
def getFatalMCOperators():
    data=[]
    queryOperator='select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD=11 and DR_INJSEVER=5'
    queryPassenger='select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD=11 and P1_INJSEVER=5'
    #query=db.session.query(fatalities.year, db.func.count(fatalities.crsh_num).label('total')).filter(fatalities.dr_inj_severity=='4').order_by(fatalities.year)
    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            queryOperator=queryOperator+' group by month(evnt_crsh_dt) order by month'
            queryPassenger=queryPassenger+' group by month(evnt_crsh_dt) order by month'
    else:
        if 'year' in request.args:
            yr=request.args['year']
            queryOperator=queryOperator+ ' and cal_yr in ('+yr+')'
            queryPassenger=queryPassenger+ ' and cal_yr in ('+yr+')'          
        if 'county' in request.args:
            county=request.args['county']
            queryOperator=queryOperator+' and contydot='+county
            queryPassenger=queryPassenger+' and contydot='+county
        if 'district' in request.args:
            district=request.args['district']
            queryOperator=queryOperator+' and mandist='+district
            queryPassenger=queryPassenger+' and mandist='+district
        queryOperator=queryOperator+' group by month(evnt_crsh_dt) order by month'
        queryPassenger=queryPassenger+' group by month(evnt_crsh_dt) order by month'

        print("queryOperator--->"+queryOperator)

    with engine.connect() as con:
        #rs= con.execute('select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD in (11) and DR_INJSEVER=4 and cal_yr between 2016 and 2018 group by month(evnt_crsh_dt) order by month')
        rs= con.execute(queryOperator)
        #rs1= con.execute('select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD in (11) and P1_INJSEVER=4 and cal_yr between 2016 and 2018 group by month(evnt_crsh_dt) order by month')
        rs1= con.execute(queryPassenger)
        for row,row1 in zip(rs,rs1):
            print(row[0],row[1],row1[1])
            data.append({'month':row[0],'fatal_mcOperator':int(row[1]),'fatal_mcPassenger':int(row1[1])})
    resp= app.response_class(
        response=json.dumps(data),
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

"""API to query database to get severe injured MC Operators"""
@app.route("/api/v1/resources/getInjuredOperators", methods=['GET'], endpoint='getInjuredOperators')
def getInjuredOperators():
    data=[]
    queryOperator='select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD=11 and DR_INJSEVER=4'
    queryPassenger='select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD=11 and P1_INJSEVER=4'
 
    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            queryOperator=queryOperator+' group by month(evnt_crsh_dt) order by month'
            queryPassenger=queryPassenger+' group by month(evnt_crsh_dt) order by month'
    else:
        if 'year' in request.args:
            yr=request.args['year']
            queryOperator=queryOperator+ ' and cal_yr in ('+yr+')'
            queryPassenger=queryPassenger+ ' and cal_yr in ('+yr+')'         
        if 'county' in request.args:
            county=request.args['county']
            queryOperator=queryOperator+' and contydot='+county
            queryPassenger=queryPassenger+' and contydot='+county
        if 'district' in request.args:
            district=request.args['district']
            queryOperator=queryOperator+' and mandist='+district
            queryPassenger=queryPassenger+' and mandist='+district
        queryOperator=queryOperator+' group by month(evnt_crsh_dt) order by month'
        queryPassenger=queryPassenger+' group by month(evnt_crsh_dt) order by month'

    with engine.connect() as con:
        #rs= con.execute('select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD in (11) and DR_INJSEVER=4 and cal_yr between 2016 and 2018 group by month(evnt_crsh_dt) order by month')
        rs= con.execute(queryOperator)
        #rs1= con.execute('select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD in (11) and P1_INJSEVER=4 and cal_yr between 2016 and 2018 group by month(evnt_crsh_dt) order by month')
        rs1= con.execute(queryPassenger)
        for row,row1 in zip(rs,rs1):
            print(row[0],row[1],row1[1])
            data.append({'month':row[0],'fatal_mcOperator':int(row[1]),'fatal_mcPassenger':int(row1[1])})
    resp= app.response_class(
        response=json.dumps(data),
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/api/v1/resources/getByDayOfWeek", methods=['GET'], endpoint='byDayOfweek')
def byDayOfweek():
    data=[]
    queryFatal='select dayofweek(evnt_crsh_dt) as day_of_week ,count(*) from fatalities  where DR_INJSEVER=5 and VHCL_BDY_TYP_CD=11'
    queryInjury='select dayofweek(evnt_crsh_dt) as day_of_week ,count(*) from fatalities where DR_INJSEVER=4 and VHCL_BDY_TYP_CD=11'
 
    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            queryFatal=queryFatal+' group by day_of_week having day_of_week not in (1,7) order by day_of_week'
            queryInjury=queryInjury+' group by day_of_week having day_of_week not in (1,7) order by day_of_week'
    else:
        if 'year' in request.args:
            yr=request.args['year']
            queryFatal=queryFatal+ ' and cal_yr in ('+yr+')'
            queryInjury=queryInjury+ ' and cal_yr in ('+yr+')'         
        if 'county' in request.args:
            county=request.args['county']
            queryFatal=queryFatal+' and contydot='+county
            queryInjury=queryInjury+' and contydot='+county
        if 'district' in request.args:
            district=request.args['district']
            queryFatal=queryFatal+' and mandist='+district
            queryInjury=queryInjury+' and mandist='+district
        queryFatal=queryFatal+' group by day_of_week having day_of_week not in (1,7) order by day_of_week'
        queryInjury=queryInjury+' group by day_of_week having day_of_week not in (1,7) order by day_of_week'

    with engine.connect() as con:
        #rs= con.execute('select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD in (11) and DR_INJSEVER=4 and cal_yr between 2016 and 2018 group by month(evnt_crsh_dt) order by month')
        rs= con.execute(queryFatal)
        #rs1= con.execute('select month(evnt_crsh_dt) as month , round(count(*)/3) from fatalities where VHCL_BDY_TYP_CD in (11) and P1_INJSEVER=4 and cal_yr between 2016 and 2018 group by month(evnt_crsh_dt) order by month')
        rs1= con.execute(queryInjury)
        for row,row1 in zip(rs,rs1):
            print(row[0],row[1],row1[1])
            data.append({'week':row[0],'fatal':int(row[1]),'injured':int(row1[1])})
    resp= app.response_class(
        response=json.dumps(data),
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp



"""Map related APIs"""
@app.route("/api/v1/resources/getmcInjuryByCounty", methods=['GET'], endpoint='getmcInjury')
def getmcInjury():
    data=[]
    queryString="select contydot, county_name, count(*) from  fatalities,counties where contydot=county_id  and  DR_INJSEVER=4 and VHCL_BDY_TYP_CD=11"

    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            queryString=queryString+'  group by CONTYDOT order by CONTYDOT'
    else:
        if 'year' in request.args:
            yr=request.args['year']
            queryString=queryString+ ' and cal_yr in ('+yr+')'         
        if 'county' in request.args:
            county=request.args['county']
            queryString=queryString+' and contydot='+county
        if 'district' in request.args:
            district=request.args['district']
            queryString=queryString+' and mandist='+district
        queryString=queryString+'  group by CONTYDOT order by CONTYDOT'

    with engine.connect() as con:
        rs= con.execute(queryString)
 
        for row in rs:
            print(row[0],row[1],row[2])
            data.append({'county_id':row[0],'county_name':row[1],'injured':int(row[2])})
    resp= app.response_class(
        response=json.dumps(data),
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/api/v1/resources/getmcFatalityByCounty", methods=['GET'], endpoint='getmcFatality')
def getmcFatality():
    data=[]
    queryString="select contydot, county_name, count(*) from  fatalities,counties where contydot=county_id  and  DR_INJSEVER=5 and VHCL_BDY_TYP_CD=11"

    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            queryString=queryString+'  group by CONTYDOT order by CONTYDOT'
    else:
        if 'year' in request.args:
            yr=request.args['year']
            queryString=queryString+ ' and cal_yr in ('+yr+')'         
        if 'county' in request.args:
            county=request.args['county']
            queryString=queryString+' and contydot='+county
        if 'district' in request.args:
            district=request.args['district']
            queryString=queryString+' and mandist='+district
        queryString=queryString+'  group by CONTYDOT order by CONTYDOT'

    with engine.connect() as con:
        rs= con.execute(queryString)
 
        for row in rs:
            print(row[0],row[1],row[2])
            data.append({'county_id':row[0],'county_name':row[1],'fatalities':int(row[2])})
    resp= app.response_class(
        response=json.dumps(data),
        mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run(debug=True)