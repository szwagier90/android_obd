	var directionsDisplay;
	var directionsService = new google.maps.DirectionsService();
	var map;
	var waypts = [];

	var tmarker=[];

	var i=0;
	var spalanie=[];
	var predkosc=[];
	var id=[];
	for(i=0; i<aaa.length; i++)
	{
		id.push(aaa[i].id);
		if(aaa[i].spalanie>0) spalanie.push(aaa[i].spalanie);
		else spalanie.push(0);
		if(aaa[i].predkosc>0) predkosc.push(aaa[i].predkosc);
		else predkosc.push(0);
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
                valueSuffix: 'j'
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
                   }
               }
           },

        });
    });

	  
      function initialize() {
		directionsDisplay = new google.maps.DirectionsRenderer();
        var mapOptions = {
          center: new google.maps.LatLng(aaa[0].X, aaa[0].Y),
          zoom: 6
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
			var spalanie = aaa.spalanie;
			var predkosc = aaa.predkosc;
			
			var marker = new google.maps.Marker({
			position: way,
			icon: {
				path: google.maps.SymbolPath.CIRCLE,
				scale: 3
			},
			draggable: false,
			map: map,
			animation: google.maps.Animation.DROP
			});
			tmarker.push(marker);

		
            var contentString = '<p>wspolrzedne: '+way+'<p>spalanie: '+spalanie+'<p> predkosc: '+predkosc;

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
