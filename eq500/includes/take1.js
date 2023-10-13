// cf. https://www.w3.org/wiki/Dynamic_style_-_manipulating_CSS_with_JavaScript
// https://www.webplatform.org/

var t1;

var r;
var b;
var g;
var bgColorStr;
var fgColorStr;

var intrvl;


function chgit(){
	var body_el = document.getElementById("bdy");
	calcVals();
	body_el.style.backgroundColor = bgColorStr;
	t1 = setTimeout(chgit,intrvl)
}

function calcVals(){
	intrvl = Math.floor((Math.random() * 5000) + 1000);
	r = Math.floor(Math.random() * 255).toString(16);
	g = Math.floor(Math.random() * 255).toString(16);
	b = Math.floor(Math.random() * 255).toString(16);
	bgColorStr = '#' + r + g + b;
	fgColorStr = '#' + b + g + r;
	
//	alert(intrvl + "\n" + bgColorStr);
}














