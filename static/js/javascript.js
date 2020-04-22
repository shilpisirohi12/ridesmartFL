

window.onload=$(function() {
    $('select#county').bind('change', function() {
      $.getJSON('/_background_process', {
        district: $(this).children("option:selected").val(),
      }, function(data) {
       // $("#result").text(data.result);
       console.log(data.result)
      });
      return false;
    });
  });

  //graphs
  google.load("visualization", "1", {packages:["corechart"]});
  google.setOnLoadCallback(drawVisualization);

  function drawVisualization() {
 // Some raw data (not necessarily accurate)
    var dataFatalities = google.visualization.arrayToDataTable([
    ['Year','MC Fatalities','Fatalities'],
    {% for d,tt in zip(mc_data,traffic) %}
        ['{{d.year}}',parseInt('{{d.fatalities}}'),parseInt('{{tt.fatalities}}')],
    {% endfor %}
    ]);

    // var dataProportions= google.visualization.arrayToDataTable([
    // ['Year','Proportion of MC crashes in Traffic Crashes','Proportion of MC Fatalities in Traffic Fatalities'],
    // {% for p in proportions %}
    //   ['{{p.year}}',parseInt('{{p.fatalities}}'),parseFloat('{{p.fatalities}}')],
    // {% endfor %}
    // ]);
    var dataProportions = google.visualization.arrayToDataTable([
    ['Year','Proportion of MC crashes in Traffic Crashes','Proportion of MC Fatalities in Traffic Fatalities'],
    ['2011',3.2,18.8],
    ['2012',3.8,18.8],
    ['2013',3.3,19.2],
    ['2014',3.1,18],
    ['2015',2.9,19.9],
    ['2016',2.7,17.2],
    ['2017',2.6,17.7],
    ['2018',2.4,17.1]
    ]);

    var injuredByMonth = google.visualization.arrayToDataTable([
    ['Month','MC Operators Injured','MC Passengers Injured'],
    {% for data in injuredAverage %}
        ['{{data.month}}',parseInt('{{data.fatal_mcOperator}}'),parseInt('{{data.fatal_mcPassenger}}')],
      {% endfor %}
    ]);

    var fatalByMonth = google.visualization.arrayToDataTable([
    ['Month','MC Operators Killed','MC Passengers killed'],
    {% for data in fatalAverage %}
        ['{{data.month}}',parseInt('{{data.fatal_mcOperator}}'),parseInt('{{data.fatal_mcPassenger}}')],
      {% endfor %}
    ]);

var optionsFatalities = {
  title : 'Motorcycle Fatalities in Florida (2011 to 2019)',
  vAxes: {0: {title: 'Motorcycle Fatalities',minValue: 0, titleTextStyle:{  bold: 0,  italic: 0 }},
          1: {title: 'Traffic Fatalities',minValue: 0, titleTextStyle:{  bold: 0,  italic: 0 }}},
  hAxis: {title: '', titleTextStyle:{  bold: 1,  italic: 0 }, format: "", minValue: 2000, maxValue: 2018, ticks: [2011,2012,2013,2014,2015,2016,2017,2018, 2019 ],textStyle : { fontSize: 9  },  
    slantedText: false, slantedTextAngle:90},
  seriesType: 'bars',
  series: {0: {targetAxisIndex:0, type:'bars'},
  1: {targetAxisIndex:1, type: 'line', pointShape: 'circle',color: 'blue',pointSize: 8,lineWidth: 2},
  0:{color: 'red'}
  },
  legend: { position: 'bottom' },
  backgroundColor: '#A2A2A2',
};

var optionsProportions = {
  // chartArea:{width:'85%'},
    title : 'Proportion of Motorcycle (MC) Crashes and Fatalities in Florida (2011-2019)',
    vAxis: {title: 'Values in Percentage(%)',titleTextStyle:{  bold: 1,  italic: 0 }},
    hAxis: {title: '', titleTextStyle:{  bold: 1,  italic: 0 }, format: "", minValue: 2000, maxValue: 2018, ticks: [2011,2012,2013,2014,2015,2016,2017,2018,2019 ],textStyle : { fontSize: 9 },  
      slantedText: false, slantedTextAngle:90},
    seriesType: 'lines',
    series: { 0:{pointShape: 'circle',pointSize: 8,lineWidth: 2},
    1:{pointShape: 'circle',pointSize: 8,lineWidth: 2}},
    legend: { position: 'bottom' },
    backgroundColor: '#A2A2A2',
    
  };

  var optionsinjuredByMonth = {
      //chartArea:{width:'85%'},
    title : 'Seriously Injured Motorcyclists by Month (2016-2018 Average)',
    vAxis: {title: '',titleTextStyle:{  bold: 1,  italic: 0 }},
    hAxis: {title: '', titleTextStyle:{  bold: 1,  italic: 0 }, format: "", minValue: 2000, maxValue: 2018, ticks: [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018 ],textStyle : { fontSize: 9  },  
      slantedText: false, slantedTextAngle:90},
    seriesType: 'bars',
    isStacked: true,
    legend: { position: 'bottom' },
    backgroundColor: '#A2A2A2',
    
  };

  var optionsfatalByMonth = {
      //chartArea:{width:'85%'},
    title : 'Motorcycle(MC) Fatalities by Month (2016-2018 Average)',
    vAxis: {title: '',titleTextStyle:{  bold: 1,  italic: 0 }},
    hAxis: {title: '', titleTextStyle:{  bold: 1,  italic: 0 }, format: "", minValue: 2000, maxValue: 2018, ticks: [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018 ],textStyle : { fontSize: 9  },  
      slantedText: false, slantedTextAngle:90},
    seriesType: 'bars',
    isStacked: true,
    legend: { position: 'bottom' },
    backgroundColor: '#A2A2A2',
    
  };    

var chartFatalities = new google.visualization.ComboChart(document.getElementById('Fatalities'));
chartFatalities.draw(dataFatalities, optionsFatalities);

var chartProportions = new google.visualization.ComboChart(document.getElementById('proportions'));
chartProportions.draw(dataProportions, optionsProportions);

var chartInjuredByMonth = new google.visualization.ComboChart(document.getElementById('injuredByMonth'));
chartInjuredByMonth.draw(injuredByMonth, optionsinjuredByMonth);

var chartFatalByMonth = new google.visualization.ComboChart(document.getElementById('fatalByMonth'));
chartFatalByMonth.draw(fatalByMonth, optionsfatalByMonth);
}
