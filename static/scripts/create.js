  /*                    /
 / Variable definition /
/                    */
var colour = "rgb(255, 255, 255)"
var row;
var rows;
var state = 0;
var wide = 15;
var coords;

/*Function definition*/
function updateRows(state, element) {
	/*gets the coordinates of the cell that has just been clicked*/
    coords = [element.x.animVal.value / wide, element.y.animVal.value / wide];
	/*updates the row grid to reflect the new state of that cell*/
    rows[coords[1]][coords[0]] = state;
}

function post() {
    var form = document.getElementById("nonogram");
    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "data");
    hiddenField.setAttribute("value", rows);
    form.appendChild(hiddenField);
    form.submit();
}

function colourChange(element) {
	/*checks to see what the current colour of the cell is*/
    if (element.style.fill == "rgb(255, 255, 255)"){
		/*flips it's colour*/
		/*updates the state and colour variablke accordingly*/
        colour = "rgb(0, 0, 0)";
        state = 1;
		/*updates the cell's fill*/

        element.style.fill = colour;
        updateRows(state, element);
    }
    else {
        colour = "rgb(255, 255, 255)";
        state = 0;
        element.style.fill = colour;
        updateRows(state, element);
    }
}

function continuedColourChange(element, colour) {
    element.style.fill = colour;
    updateRows(state, element);
}

function drawGrid(width, height, wide) {
	if (confirm("Warning, if you have already started drawing this will clear your progress!") == true) {
		var element = document.getElementById("svg");
		var save = document.getElementById("save");
		element.parentNode.removeChild(element);
		var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
		var svgNS = svg.namespaceURI;
		save.setAttribute('style', 'display:inline;')
		console.log(save)

		rows = [];
		for (y = 0; y < height; y++) {
			row = [];
			for (x = 0; x < width; x++) {
				row.push(0);
				var rect = document.createElementNS(svgNS, 'rect')
				rect.setAttribute('onmousedown', 'colourChange(this)');
				rect.setAttribute('x', wide * x);
				rect.setAttribute('y', wide * y);
				rect.setAttribute('style','fill:#ffffff; cursor:pointer;');
				rect.setAttribute('width', wide);
				rect.setAttribute('height', wide);
				rect.setAttribute('stroke','#000000');
				rect.addEventListener("mouseover", function(e){
					if(e.buttons == 1 || e.buttons == 3){
						continuedColourChange(this, colour);
						}
					})
				svg.appendChild(rect);
				document.getElementById('grid').appendChild(svg);
        document.getElementById('grid').setAttribute('width', wide);
        document.getElementById('grid').setAttribute('height', wide);
			}
			rows.push(row);
		}
		console.log(rows);
		svg.setAttribute('width',  wide * width);
		svg.setAttribute('height', wide * height);
		svg.setAttribute('id', 'svg');
	}
}
