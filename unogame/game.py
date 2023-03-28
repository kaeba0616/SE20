
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

drawing = svg2rlg("resources/images/card/normalMode/plus4/all4.svg")
renderPM.drawToFile(drawing, 'resources/images/output.png', fmt='PNG')
