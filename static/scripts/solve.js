  /*                    /
 / Variable definition /
/                    */
var colour = "rgb(0, 0, 0)"
var row;
var rows;
var state = 0;
var wide = 15;
var coords;

function format2D(a) {
    var str="";
    for (var i = 0; i<a.length; i++) {
        str+=a[i].toString()+"<br/>";
    }
    str=str.substr(0,str.length-1);
    return str;
}

/*Function definition*/
function updateRows(state, element) {
	/*gets the coordinates of the cell that has just been clicked*/
	coords = JSON.parse(element.id);
	/*updates the row grid to reflect the new state of that cell*/
	rows[coords[1]][coords[0]] = state;
}

function colourChange(element) {
	/*checks to see what the current colour of the cell is*/
		if (element.style.fill == "rgb(0, 0, 0)"){
		/*flips it's colour*/
		/*updates the state and colour variable accordingly*/
				colour = "rgb(255, 255, 255)";
				state = 0;
		/*updates the cell's fill*/
				element.style.fill = colour;
				updateRows(state, element);
		}
		else {
				colour = "rgb(0, 0, 0)";
				state = 1;
				element.style.fill = colour;
				updateRows(state, element);
		}
}

function continuedColourChange(element, colour) {
		element.style.fill = colour;
		updateRows(state, element);
}

var puzzleTemplate = document.getElementById('puzzle_temp');
puzzleTemplate.addEventListener("mouseover", dragged, false);

function dragged(e) {
		if (e.target !== e.currentTarget) {
				if (e.target.id != ""){
					if(e.buttons == 1 || e.buttons == 3){
						continuedColourChange(e.target, colour);
					};
				}
		}
		e.stopPropagation();
}
