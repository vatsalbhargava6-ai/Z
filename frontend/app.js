let lat = 0;
let lng = 0;
let marker = null;

let history = [];
let historyIndex = -1;


// ---------------- MAP ----------------

let map = L.map('map').setView(
  [22.9734,78.6569],
  5
);


L.tileLayer(
'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
{
 attribution:'Z Land Engine'
}
).addTo(map);



// ---------------- MARKER ----------------

function setMarker(lat,lng){

    if(marker){
        map.removeLayer(marker);
    }

    marker = L.marker([lat,lng])
    .addTo(map)
    .bindPopup("🌍 Analysis Point")
    .openPopup();

}



// ---------------- ADDRESS ----------------

async function getAddress(lat,lng){

try{

let res = await fetch(
`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
);

let data = await res.json();

return data.display_name || "Unknown";

}
catch{

return "Unknown";

}

}



// ---------------- HISTORY ----------------

function saveLocation(lat,lng,address){

history.push({
lat,
lng,
address
});

historyIndex = history.length-1;

}




function goBack(){

if(historyIndex<=0){
alert("No previous location");
return;
}


historyIndex--;

let loc = history[historyIndex];


lat = loc.lat;
lng = loc.lng;


map.setView([lat,lng],15);

setMarker(lat,lng);


document.getElementById("selected").innerHTML=`

📍 <b>${loc.address}</b><br>

Lat: ${lat.toFixed(6)}<br>
Lng: ${lng.toFixed(6)}

`;


runPipeline();

}





// ---------------- MAP CLICK ----------------


map.on(
'click',
async function(e){


lat=e.latlng.lat;
lng=e.latlng.lng;


setMarker(lat,lng);


let address =
await getAddress(lat,lng);


saveLocation(lat,lng,address);



document.getElementById("selected").innerHTML=`

📍 <b>${address}</b><br>

🌐 Lat: ${lat.toFixed(6)}<br>

🌐 Lng: ${lng.toFixed(6)}

`;



runPipeline();


});




// ---------------- SEARCH ----------------


async function searchPlace(){


let q =
document.getElementById("search").value;


if(!q)return;



let res =
await fetch(

`https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${q}`

);



let data =
await res.json();



if(!data.length){

alert("Not found");
return;

}



lat=parseFloat(data[0].lat);
lng=parseFloat(data[0].lon);



map.setView(
[lat,lng],
15
);



setMarker(lat,lng);



let address =
await getAddress(lat,lng);



saveLocation(
lat,
lng,
address
);



document.getElementById("selected").innerHTML=`

📍 <b>${address}</b><br>

🌐 Lat: ${lat.toFixed(6)}<br>

🌐 Lng: ${lng.toFixed(6)}

`;



runPipeline();


}




// ---------------- AI PIPELINE ----------------


async function runPipeline(){


let aiBox =
document.getElementById("ai");


let zoneBox =
document.getElementById("zone");



aiBox.innerHTML =
"🛰 Satellite + AI analysing...";



try{


let res =
await fetch("/analyze",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},


body:JSON.stringify({

lat,
lng

})


});



let data =
await res.json();



aiBox.innerHTML = `


<h3>🌦 WEATHER</h3>

<p>
🌡 Temperature:
${data.temperature} °C
</p>


<p>
☁ Condition:
${data.condition}
</p>


<p>
🌧 Rain:
${data.rain}
</p>



<hr>


<h3>🛰 SATELLITE AI</h3>


<p>
NDVI:
${data.ndvi}
</p>


<p>
Vegetation:
${data.vegetation}
</p>




<hr>



<h3>🌍 LAND DETECTION</h3>


<p>
Type:
<b>${data.land_type}</b>
</p>


<p>
Confidence:
${data.confidence}
</p>




<hr>



<h3>🌾 CROP HEALTH</h3>


<p>
${data.crop}
-
${data.health_status}
</p>


<p>
Score:
${data.crop_health_score}
</p>




<hr>



<h3>🤖 GEMINI AGRI AI</h3>


<p>

${data.ai_report || 
"Gemini analysing..."}

</p>


`;



zoneBox.innerHTML =
(data.zones||[]).join("<br>");



}

catch(err){

console.log(err);

aiBox.innerHTML =
"❌ Backend Error";

}


}