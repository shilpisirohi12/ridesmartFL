from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine

#Setting up the app
app=Flask(__name__)
app.jinja_env.globals.update(zip=zip)
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://shilpi:shilpi@127.0.0.1:3306/ridesmartfl'
engine=create_engine('mysql://shilpi:shilpi@127.0.0.1:3306/ridesmartfl')
conn=engine.connect()
#db=SQLAlchemy(app)


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
countyName=['Charlotte',
'Citrus',
'Collier',
'Desoto',
'Glades',
'Hardee',
'Hendry',
'Hernando',
'Highlands',
'Hillsborough',
'Lake',
'Lee',
'Manatee',
'Pasco',
'Pinellas',
'Polk',
'Sarasota',
'Sumter',
'Alachua',
'Baker',
'Bradford',
'Columbia',
'Dixie',
'Gilchrist',
'Hamilton',
'Lafayette',
'Levy',
'Madison',
'Marion',
'Suwannee',
'Taylor',
'Union',
'Bay',
'Calhoun',
'Escambia',
'Franklin',
'Gadsden',
'Gulf',
'Holmes',
'Jackson',
'Jefferson',
'Leon',
'Liberty',
'Okaloosa',
'Santa Rosa',
'Wakulla',
'Walton',
'Washington',
'Brevard',
'Clay',
'Duval',
'Flagler',
'Nassau',
'Orange',
'Putnam',
'Seminole',
'St Johns',
'Volusia',
'Broward',
'Miami-Dade',
'Indian River',
'Martin',
'Monroe',
'Okeechobee',
'Osceola',
'Palm Beach',
'St Lucie']

@app.route('/dashboard', methods=['GET','POST'])
def start():
    query="SELECT CAL_YR as year,COUNT(*) as cnt  FROM FATALITIES WHERE "
    if request.method=='POST':
        year_selected=request.form.get('year')
        dist_selected=request.form.get('district')
        county_selected=request.form.get('county')
        temp_var=0
        if dist_selected != 0:
            query=query+ " MANDIST="+dist_selected
            temp_var=1
        if county_selected != 0:
            if temp_var>0:
                query=query+ " and CONTYDOT= "+county_selected
            else:
                query=query+ " CONTYDOT= "+county_selected
        if temp_var>0:
            query=query+" AND DR_INJSEVER=:SEVERITY AND VHCL_BDY_TYP_CD=:BODY_TYP GROUP BY CAL_YR;"
        else:
            query=query+" DR_INJSEVER=:SEVERITY AND VHCL_BDY_TYP_CD=:BODY_TYP GROUP BY CAL_YR;"
    else:
        query=query+" DR_INJSEVER=:SEVERITY AND VHCL_BDY_TYP_CD=:BODY_TYP GROUP BY CAL_YR;"    

        print(query)
    stmt = text(query)
    stmt = stmt.columns(fatalities.crsh_num, fatalities.year, fatalities.dist_code, fatalities.county_code)
    DataDict=conn.execute(stmt,SEVERITY='5',BODY_TYP='11').fetchall()

 
    return render_template('dashboard.html',data=DataDict,years=year,districts=district,counties=countyName)


if __name__ == "__main__":
    app.run(debug=True)