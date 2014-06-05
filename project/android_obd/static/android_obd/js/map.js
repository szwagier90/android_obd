	var directionsDisplay;
	var directionsService = new google.maps.DirectionsService();
	var map;
	var waypts = [];

	var tmarker=[];

	var i=0;
	//var spalanie=[];
	var predkosc=[];
	var id=[];
	var timestamp=[];
	var AccX =[];
	var AccY =[];
	var AccZ =[];
	var rotation = [];
	var Z = [];
	var zakres;
	zakres = (aaa.length/10);

	for(i=0; i<aaa.length; i++)
	{
		id.push(aaa[i].id);
		//predkosc.push(aaa[i].speed);
		//if(aaa[i].AccX=='None')
		//	{AccX.push(null);}
		//else{AccX.push(aaa[i].AccX);}
		test(aaa[i].speed,predkosc);
		test(aaa[i].AccX,AccX);
		test(aaa[i].AccY,AccY);
		test(aaa[i].AccZ,AccZ);
		test(aaa[i].rotation,rotation);
		test(aaa[i].altitude,Z);
		//AccY.push(aaa[i].AccY);
		//AccZ.push(aaa[i].AccZ);
		//rotation.push(aaa[i].rotation);
		//Z.push(aaa[i].altitude);
	}

	function test(x, tab){

		if(x=='brak danych')
			{tab.push(null);}
		else{tab.push(x);}		
	}
	$(function () {

		for(i=0; i<aaa.length; i++)
		{
			timestamp.push(Highcharts.dateFormat('%H:%M:%S',aaa[i].time));
		}
        $('#container').highcharts({
            title: {
                text: 'Przeglad trasy',
                x: -20 //center
            },
            subtitle: {
                text: Highcharts.dateFormat('%e. %b %Y, %H:%M:%S',aaa[0].time)+'-'+Highcharts.dateFormat('%e. %b %Y, %H:%M:%S',aaa[timestamp.length-1].time),
                x: -20
            },
            xAxis: {
                categories: timestamp,
                tickInterval: zakres,
                type: 'datetime',
                tickmarkPlacement: 'on'

            },
            yAxis: {
                title: {
                    text: ''
                },
                //min: 0,
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
           // tooltip: {
           //     valueSuffix: ''
           // },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [
            {
                name: 'PrzyspieszenieX',
                data: AccX,
                lineWidth : 1
            },
	    	{
				name: "predkosc [m/s]",
				data: predkosc,
				lineWidth : 1
	    	},
	    	{
                name: 'PrzyspieszenieY',
                data: AccY,
                lineWidth : 1
            },
            {
                name: 'PrzyspieszenieZ',
                data: AccZ,
                lineWidth : 1
            },
            {
                name: 'Kąt względem PN',
                data: rotation,
                lineWidth : 1
            },
            {
                name: 'Wysokość n.p.m.',
                data: Z,
                lineWidth : 1
            }],
	    plotOptions: {
                series: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            mouseOver: function() {
				//infowindow.setContent(tmarker[this.x].icon.scale);
                		//infowindow.open(map,tmarker[this.x]);
					var y = id.indexOf(this.x);
				//infowindow.open(map,tmarker[y]);
           		 	tmarker[y].setAnimation(google.maps.Animation.BOUNCE);

			    },
			    mouseOut: function() {
				tmarker[this.x].setAnimation(null);
			    } 
                        }
                   },
                   marker: {
                   	radius: 3,
            		enabled: true
        		},
        		connectNulls: true
               }
           },

        });
    });

	  
      function initialize() {
		directionsDisplay = new google.maps.DirectionsRenderer();
        var mapOptions = {
          center: new google.maps.LatLng(aaa[0].X, aaa[0].Y),
          zoom: 12
        };
        map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);
		directionsDisplay.setMap(map);
		//zakladamy ze sciagamy z bazy danych do dwoch tablic (jedna - wspolrzedne, druga - pozostale) postaci:
		// wspolrzedne, 
		//spalanie: liczba
		//predkosc: liczba
		// itd...
		//*************************************************************************************
		var contentString = "";
		
		setMarkers(map,aaa);
		infowindow = new google.maps.InfoWindow({
			content: contentString
		});
	
      }
	  
	  function setMarkers(map,aaa) {
			for (var i = 0; i < aaa.length; i++) {
				setMarker(map,aaa[i]);
			}
	}

	function setMarker(map, aaa) {       
			var way = new google.maps.LatLng(aaa.X, aaa.Y);
			//var spalanie = aaa.spalanie;
			var predkosc = aaa.speed;
			var przyspieszenie = aaa.AccX;
			var marker = new google.maps.Marker({
			position: way,
			icon: {
				path: google.maps.SymbolPath.CIRCLE,
				scale: 2
			},
			draggable: false,
			map: map,
			animation: google.maps.Animation.DROP
			});
			tmarker.push(marker);

		
            var contentString = '<div style="width:250px; height:100px;">' +
    '<table border="0" cellpadding="0" cellspacing="0">' +
    '<tr>'+
    '<th scope="row">Wysokość n.p.m.: </th>' +
    '<td> '+aaa.Z+' [m]</td>' +
    '</tr>' +
    '<tr>'+
    '<th scope="row">Predkosc:</th>' +
    '<td>'+ predkosc +' [m/s]</td>' +
    '</tr>' +
    '<tr>'+
    '<th scope="row">Przyspieszenie:</th>' +
    '<td>'+ przyspieszenie +' [m/s2]</td>' +
    '</tr>' +
    '</table></div>';


            //'<p>wspolrzedne: ('+aaa.X +','+aaa.Y+')'+'<p> predkosc: '+predkosc+'<br>';

            google.maps.event.addListener(tmarker[aaa.id], "mouseover", function () {
			infowindow.setContent(contentString);
               		infowindow.open(map,tmarker[aaa.id]);
            });
	    google.maps.event.addListener(tmarker[aaa.id], "mouseout", function () {
			infowindow.setContent(contentString);
                	infowindow.close(map,tmarker[aaa.id]);
            });
        } 
	 
google.maps.event.addDomListener(window, 'load', initialize);
