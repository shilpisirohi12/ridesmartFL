from flask import Flask,render_template,request,redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests

#Setting up the app
app=Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.secret_key='cutr_usf'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://shilpi:shilpi@127.0.0.1:3306/ridesmartfl'
#engine=create_engine('mysql://shilpi:shilpi@127.0.0.1:3306/ridesmartfl')
#conn=engine.connect()
db=SQLAlchemy(app)
URL='http://127.0.0.1:5000'


#Fetching data from DB 
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

@app.route('/dashboard', methods=['GET','POST'])
def start():
    query="SELECT CAL_YR as year,COUNT(*) as cnt  FROM FATALITIES WHERE "
    params={}
    requestURL=URL+'/api/v1/resources/getFatalities'
    print(requestURL)
    if request.method=='POST':
        year_selected=request.form.get('year')
        dist_selected=request.form.get('district')
        county_selected=request.form.get('county')

        """Setting values for parameters"""
        if int(year_selected) > 0:
            params['year']=year_selected
        if int(dist_selected) > 0:
            params['district']=dist_selected
        if int(county_selected) > 0:
            params['county']=county_selected
        if int(year_selected)==0 and int(dist_selected)==0 and int(county_selected)==0:
            params['query']='all'
    else:
        params['query']='all'
        
    res=requests.get(requestURL,params=params)        
    print(res.text)
    return render_template('dashboard.html',mc_data=json.loads(res.text),years=year,districts=district,counties=countyName)

@app.route("/api/v1/resources/getFatalities", methods=['GET'])
def getFatalities():
    data=[]
    query=db.session.query(fatalities.year, db.func.count(fatalities.crsh_num).label('total')).filter(fatalities.dr_inj_severity=='5').filter(fatalities.body_type=='11')
    if 'query' in request.args:
        res=request.args['query']
        if res.lower() == 'all':
            fatality_result=query.group_by(fatalities.year).all()
    else:        
        if 'year' in request.args:
            yr=request.args['year']
            query=query.filter(fatalities.year==yr)
        if 'county' in request.args:
            county=request.args['county']
            query=query.filter(fatalities.county_code==county)
        if 'district' in request.args:
            district=request.args['district']
            query=query.filter(fatalities.dist_code==district)
        fatality_result=query.group_by(fatalities.year).all()
    for res in fatality_result:
        print(res)
        data.append({'year':res.year,'fatalities':res.total})
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)