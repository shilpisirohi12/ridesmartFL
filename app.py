from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

#Setting up the app
app=Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://shilpi:shilpi@127.0.0.1:3306/ridesmartfl'
db=SQLAlchemy(app)

#Fetching data from DB 
class Example(db.Model):
    __tablename__ = 'crash'
    crsh_num=db.Column('CRSH_NUM',db.Unicode, primary_key=True)
    year=db.Column('CAL_YR',db.Unicode)
    dist_code=db.Column('MANDIST',db.Unicode)
    county_code=db.Column('CONTYDOT',db.Unicode)
    fatalities=db.Column('TOT_OF_FATL_NUM',db.Integer)
    serious_inj=db.Column('TOT_OF_INJR_NUM',db.Integer)

    def __repr__(self):
        return self.year


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
    if request.method=='POST':
        year_selected=request.form.get('year')
        dist_selected=request.form.get('district')
        county_selected=request.form.get('county')

        if int(dist_selected)== 0 and int(year_selected)== 0 and int(county_selected) ==0:
            DataDict=Example.query.all()
        elif int(dist_selected)!= 0 and int(year_selected)== 0 and int(county_selected) !=0:
            DataDict=Example.query.filter(Example.dist_code==dist_selected).filter(Example.county_code==county_selected).all()            
        elif int(dist_selected)== 0 and int(year_selected)!= 0 and int(county_selected) !=0:
            DataDict=Example.query.filter(Example.year==year_selected).filter(Example.county_code==county_selected).all()
        elif int(dist_selected)!= 0 and int(year_selected)!= 0 and int(county_selected) ==0:
            DataDict=Example.query.filter(Example.year==year_selected).filter(Example.dist_code==dist_selected).all()            
        elif int(year_selected)== 0 and int(county_selected) ==0 and int(dist_selected)!= 0:
            DataDict=Example.query.filter(Example.dist_code==dist_selected).all()
        elif int(year_selected)!= 0 and int(county_selected) ==0 and int(dist_selected)== 0:
            DataDict=Example.query.filter(Example.year==year_selected).all()  
        elif int(year_selected)== 0 and int(county_selected) !=0 and int(dist_selected)== 0:
            DataDict=Example.query.filter(Example.county_code==county_selected).all()                       
        else:
            DataDict=Example.query.filter(Example.year==year_selected).filter(Example.dist_code==dist_selected).filter(Example.county_code==county_selected).all()
    else:
        DataDict=Example.query.all()
 
    return render_template('dashboard.html',data=DataDict,years=year,districts=district,counties=countyName)


if __name__ == "__main__":
    app.run(debug=True)