from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://shilpi:shilpi@127.0.0.1:3306/ridesmartfl'
db=SQLAlchemy(app)

class Example(db.Model):
    __tablename__ = 'test'
    id=db.Column('id',db.Integer, primary_key=True)
    name=db.Column('name',db.Unicode)


DataDict=[
    {
        'Year':'2011',
        'Fatalities':'934',
        'Serious_Injuries':'2491',
        'Total_Fatalities': '2405'

    },
    {
        'Year':'2012',
        'Fatalities':'895',
        'Serious_Injuries':'2383',
        'Total_Fatalities': '2413'

    },
        {
        'Year':'2013',
        'Fatalities':'863',
        'Serious_Injuries':'2194',
        'Total_Fatalities': '2194'

    }
]

year=['2011','2012','2013','2014','2015','2016','2017','2018']

@app.route('/dashboard', methods=['GET','POST'])
def start():
    if request.method=='POST':
        year_selected=request.form.get('year')
        print(year_selected)
        return render_template('success.html',year=year_selected)
    else:
        return render_template('dashboard.html',data=DataDict,years=year)


if __name__ == "__main__":
    app.run(debug=True)