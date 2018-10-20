from main import Graphs
from bokeh.io import output_file

el = Graphs("Floods")

output_file("Floods/Table Graph.html")

el.make_table("Differences between the ammount of possible scenarios" )
