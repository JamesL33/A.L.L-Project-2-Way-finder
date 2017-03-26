function createMarker(lat, long, map, info)
{
	map.addMarker({
 		icon: "http://maps.google.com/mapfiles/ms/micons/blue-dot.png",
 		lat: lat,
 		lng: long,
		infoWindow:
 		{
      		content: info
        },
		mouseover: function(e){
            this.infoWindow.open(this.map, this);
        },
        mouseout: function(e){
            this.infoWindow.close(this.map, this);
        },
		click: function(e) {
    		this.infoWindow.open(this.map, this);
 		}
	});
}

var beep = [
"Alan Berry",
"Alma",
"Armstrong Siddeley",
"Bugatti",
"Charles Ward",
"EEC",
"Ellen Terry",
"George Eliot",
"Graham Sutherland",
"Jaguar",
"James Starley",
"Library",
"Maurice Foss",
"Multi Storey Car Park",
"Priory",
"Richard Crossman",
"Sir John Laing",
"Sir William Lyons",
"Sports and Recreation Centre",
"Student Centre",
"The Hub",
"Whitefriars",
"William Morris"];

var locations = {
	"52.408141 -1.506584" : "Alan Berry",
	"52.410193 -1.500576" : "Alma",
	"52.406908 -1.499888" : "Armstrong Siddeley"
};