function createMarker(lat, long)
{
	map.addMarker(
	{
		icon: "http://maps.google.com/mapfiles/ms/micons/blue-dot.png",
		lat: 52.408141,
		lng: -1.506584
		infoWindow:
		{
			content: '<p>This is the Alan Berry Building!</p>'
		},	
		mouseover: function(e)
		{         
			this.infoWindow.open(this.map, this);
		}, 
		mouseout: function(e)
		{
			this.infoWindow.close(this.map, this)
			click: function(e)
			{
				this.infoWindow.open(this.map, this);
			}
		}
	});
}