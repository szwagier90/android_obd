var i=0;
var spalanie=[];
var predkosc=[];
var id=[];
for(i=0; i<aaa.length; i++)
{
	id.push(aaa[i].id);
	spalanie.push(aaa[i].spalanie);
	predkosc.push(aaa[i].predkosc);
//	alert(aaa[i].id)
}

$(function () {
        $('#container').highcharts({
            title: {
                text: 'jakis tam tytul',
                x: -20 //center
            },
            subtitle: {
                text: 'podtytul',
                x: -20
            },
            xAxis: {
                categories: id
            },
            yAxis: {
                title: {
                    text: 'Temperature (°C)'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: '°C'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'spalanie',
                data: spalanie
            },
	    {
		name: "predkosc",
		data: predkosc
	    }]
        });
    });

