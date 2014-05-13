	  var directionsDisplay;
	  var directionsService = new google.maps.DirectionsService();
	  var map;
	  var waypts = [];
	  
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
			map: map
		});

		
            var contentString = '<p>wspolrzedne: '+way+'<p>spalanie: '+spalanie+'<p> predkosc: '+predkosc;

            google.maps.event.addListener(marker, "mouseover", function () {
				infowindow.setContent(contentString);
                infowindow.open(map,this);
//		window.funkcja();
            });
	    google.maps.event.addListener(marker, "mouseout", function () {
				infowindow.setContent(contentString);
                infowindow.close(map,this);
            });
        } 
	  
	  google.maps.event.addDomListener(window, 'load', initialize);
