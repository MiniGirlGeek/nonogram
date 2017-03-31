  /*                    /
 / Variable definition /
/                    */
var colourIndex = 0;
var row;
var rows;
var nextState;
var wide = 15;
var coords;
var colours = ["rgb(255, 255, 255)", "rgb(35, 35, 35)", "url(#cross)"]

function format2D(a) {
    var str="";
    for (var i = 0; i<a.length; i++) {
        str+=a[i].toString()+"<br/>";
    }
    str=str.substr(0,str.length-1);
    return str;
}

/*Function definition*/
function updateRows(nextState, element) {
	coords = JSON.parse(element.id);
	rows[coords[1]][coords[0]] = colourIndex;
}

function post() {
		for (var r = 0; r < rows.length; r++) {
				for (var c = 0; c < rows[r].length; c++) {
						if (rows[r][c] == 2) {
							rows[r][c] = 0;
						}
				}
		}

		var form = document.getElementById("nonogram");
		var hiddenField = document.createElement("input");
		hiddenField.setAttribute("type", "hidden");
		hiddenField.setAttribute("name", "data");
		hiddenField.setAttribute("value", rows);
		form.appendChild(hiddenField);
		form.submit();
}

function colourChange(element) {
		coords = JSON.parse(element.id);
		var currentState = rows[coords[1]][coords[0]];
		nextState = (currentState + 1) % 3;
		colourIndex = nextState;
		updateRows(colourIndex, element)
		element.style.fill = colours[colourIndex];
}

function continuedColourChange(element, colourIndex) {
		element.style.fill = colours[colourIndex];
		updateRows(colourIndex, element);
}

var puzzleTemplate = document.getElementById('puzzle_temp');
puzzleTemplate.addEventListener("mouseover", dragged, false);

function dragged(e) {
		if (e.target !== e.currentTarget) {
				if (e.target.id != ""){
					if(e.buttons == 1 || e.buttons == 3){
						continuedColourChange(e.target, colourIndex);
					};
				}
		}
		e.stopPropagation();
}
