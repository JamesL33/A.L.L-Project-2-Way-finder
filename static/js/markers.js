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

var locations = {
	"52.408141 -1.506584" : "Alan Berry",
	"52.410193 -1.500576" : "Alma",
	"52.406908 -1.499888" : "Armstrong Siddeley",
	"52.407662 -1.503825" : "Bugatti",
	"52.408635 -1.504771" : "Charles Ward",
	"52.405482 -1.501099" : "EEC",
	"52.406799 -1.504689" : "Ellen Terry",
	"52.407812 -1.504942" : "George Eliot",
	"52.407231 -1.502662" : "Graham Sutherland",
	"52.407283 -1.504535" : "Hub",
	"52.406683 -1.501497" : "Jaguar",
	"52.407626 -1.503872" : "James Starley",
	"52.406062 -1.501317" : "Library",
	"52.407833 -1.503738" : "Maurice Foss",
	"52.406636 -1.499889" : "Multi Storey Car Park",
	"52.408497 -1.506440" : "Priory",
	"52.406827 -1.505148" : "Richard Crossman",
	"52.405529 -1.505479" : "Sir John Laing",
	"52.407121 -1.499938" : "Sir William Lyons",
	"52.406091 -1.503946" : "Sports and Recreation Centre",
	"52.404736 -1.500288" : "Student Centre",
	"52.405411 -1.501189" : "Whitefriars",
	"52.406431 -1.501569" : "William Morris"
};