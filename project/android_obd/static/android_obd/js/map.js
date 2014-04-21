//<script type="text/javascript"
     // src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDvBedZY7MOZPqbGxmkBctmNfm2ooi9xls&sensor=true">
   // </script>
   // <script type="text/javascript">
	  var directionsDisplay;
	  var directionsService = new google.maps.DirectionsService();
	  var map;
	  var waypts = [];
	  
      function initialize() {
		directionsDisplay = new google.maps.DirectionsRenderer();
        var mapOptions = {
          center: new google.maps.LatLng(-34.397, 150.644),
          zoom: 8
        };
        map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);
		directionsDisplay.setMap(map);
		//zakladamy ze <div id="map-canvas"/>sciagamy z bazy danych do dwoch tablic (jedna - wspolrzedne, druga - pozostale) postaci:
		//locations: wspolrzedne, 
		//spalanie: liczba
		//predkosc: liczba
		// itd...
		var i;
		var value; 
		value = [];
		
		var dane;
		dane = [];
		value.push(new google.maps.LatLng(aaa[0].X,aaa[0].Y));
		dane.push(aaa[0]);
		//aaa[] jest tablica z danymi :)
		for(i=1;i<aaa.length-1;i++)
		{
			value.push(new google.maps.LatLng(aaa[i].X,aaa[i].Y));
			waypts.push({location:value[i],stopover:false});
			dane.push(aaa[i]);
		}
		
		value.push(new google.maps.LatLng(aaa[aaa.length-1].X,aaa[aaa.length-1].Y));
		dane.push(aaa[aaa.length-1]);
		//*************************************************************************************
		start = value[0];//new google.maps.LatLng(aaa[0].X, aaa[0].Y);
		end = value[aaa.length-1];//new google.maps.LatLng(aaa[5].X, aaa[5].Y);
		
		calcRoute(waypts,start,end);
		waypts.unshift({location:start, stopover:false})
		waypts.push({location:end,stopover:false})
		
		//*************************************************************************************
		var contentString = "aaa";
		
		setMarkers(map,dane,waypts);
		infowindow = new google.maps.InfoWindow({
			content: contentString
		});
	
      }
	  
	  function setMarkers(map,dane,waypts) {
			for (var i = 0; i < waypts.length; i++) {
				setMarker(map,dane[i],waypts[i].location);
			}
	}

	function setMarker(map, dane, waypts) {       
			var way = waypts;
			var spalanie = dane.spalanie;
			var predkosc = dane.predkosc
			
			var marker = new google.maps.Marker({
			position: way,
			icon: {
				path: google.maps.SymbolPath.CIRCLE,
				scale: 2
			},
			draggable: false,
			map: map
		});

		
            var contentString = '<p>wspolrzedne: '+way+'<p>spalanie: '+spalanie+'<p> predkosc: '+predkosc;

            google.maps.event.addListener(marker, "mouseover", function () {
				infowindow.setContent(contentString);
                infowindow.open(map,this);
            });
        } 
	  
	  function calcRoute(waypts,start,end) {
		
	  var request = {
		origin: start,//"Halifax, NS",
		destination: end,//"Vancouver, BC",
		waypoints: waypts,
		optimizeWaypoints: false,
		travelMode: google.maps.TravelMode.DRIVING
	  };
	  
	  directionsService.route(request, function(response, status) {
		if (status == google.maps.DirectionsStatus.OK) {
			directionsDisplay.setDirections(response);
			directionsDisplay.setMap(map);
			directionsDisplay.setOptions( { suppressMarkers: true } );
		}
	  });
	}
	  google.maps.event.addDomListener(window, 'load', initialize);
  //  </script>
