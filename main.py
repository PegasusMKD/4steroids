import pandas as pd
from bokeh.plotting import figure, output_file, show
import bokeh.palettes
from bokeh.io import save
#Libraries for the Pie Chart
from math import pi 
from bokeh.transform import cumsum
#Libraries for the Table
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import components

class Graphs:

    #Initializes the class
    def __init__(self,data_set):
        self.data_set = data_set #Name of the data file that is going to be used
        self.data = {} #A dictionary used for transforming the data
    
    #Simply reads the data from a csv or excel file and it stops the program while sending a message that it won't read the file
    def read_data(self):
        try:
            self.df = pd.read_csv("%s.csv" % (self.data_set))
        except:
            try:
                self.df=pd.read_excel("%s.xlsx" % (self.data_set))
            except:
                print("Couldn't read the file...\n Please try a different file format or check if the file is in the same folder!")

    #Reading data, but with Dates being parsed in
    
    def read_data_dates(self):
        try:
            self.df = pd.read_csv("%s.csv" % (self.data_set),parse_dates=["Date"])
        except:
            try:
                self.df=pd.read_excel("%s.xlsx" % (self.data_set), parse_dates=["Date"])
            except:
                print("Couldn't read the file...\n Please try a different file format or check if the file is in the same folder!")
    
    #Makes the DataFrame into a DataSeries for easier use for the Pie Charts and some other similar categorial data
    def make_data(self,typ):
        self.read_data()
        for key_name in self.df:

            if raw_input("Do you want to add the next column '%s' for '%s'? y/n          " % (key_name,typ)) == "n":   #Makes it a lot more easier to implement whichever DataSet is desired
                continue                                                                                  #and the correct columns from it

            for value_name in self.df[key_name]:
                try:
                    value_name = int(value_name)
                except:
                    break
                if key_name in self.data.keys():
                    self.data[key_name] += int(value_name)
                else:
                    self.data.update({key_name : int(value_name)})
            
        self.df_main = pd.Series(self.data).reset_index(name="value").rename(columns={'index' : 'category_value'})
    
    #Makes a Data Table visualization of the data(similar to the make_data function, difference being making 2 more lists and implementing them for making the DataTable)
    def make_table(self,title):
        self.read_data()
        new_lst =[]
        for key_name in self.df:

            if raw_input("Do you want to add the next column '%s' for the TABLE : '%s'? y/n          " % (key_name,title)) == "n":
                continue
            new_lst.append(key_name)
            for value_name in self.df[key_name]:
                try:
                    value_name = int(value_name)
                except:
                    break
                if key_name in self.data.keys():
                    self.data[key_name] += int(value_name)
                else:
                    self.data.update({key_name : int(value_name)})
        self.source = ColumnDataSource(self.df)
        self.columns =[]
        for x in self.df.keys():
            self.columns.append(TableColumn(field = '%s' % (x), title = '%s' % (x)))
        self.data_table = DataTable(source=self.source, columns=self.columns, width=400, height=550)
        show(widgetbox(self.data_table))

    #Makes a Line Graph with x and y axis
    def make_line(self, title,x_axis,y_axis,tt):
        self.read_data()
        if raw_input("Do you want the data sorted? (y/n)") == "y":
            self.df_sorted = self.df.sort_values(by=[x_axis],ascending=True)
            self.df = self.df_sorted
        self.f = figure(plot_height=400,plot_width=600, tools="", logo=None)
        self.f.title.text = title
        self.f.title.align = "center"
        self.f.xaxis.axis_label = x_axis
        self.f.yaxis.axis_label = y_axis
        self.f.line(self.df[x_axis],self.df[y_axis])
        show(self.f)
        
    #Gets an average of some data, and transforms that same data into its average
    def get_average(self):
        if self.data == {}:
            self.make_data(title)
        new_lst = []
        
        for x in self.df_main['value']:
            if x < len(self.df):
                pass
            else:
                x = x / len(self.df)
                new_lst.append(x)
        df_1 = {'value' : new_lst }
        self.df_main.update(df_1)

    #Makes a Pie Chart
    def make_pie(self,title,tt):
        if self.data == {}:                 #Checks if the data has already been processes, if so, no need to add it twice
            self.make_data(title)
        #Turns the data into angles, which is used to seperate the categories
        self.df_main['angle'] = self.df_main['value'] / self.df_main['value'].sum() * 2*pi
        self.df_main['color'] = bokeh.palettes.viridis(len(self.data))
        self.p = figure(plot_height=550,plot_width=550, tools="hover", toolbar_location=None, logo=None, tooltips = tt)
        self.p.wedge(x=0, y=1, radius=0.4, start_angle = cumsum('angle', include_zero=True), end_angle=cumsum('angle'),line_color="white", fill_color='color', legend='category_value', source=self.df_main)
        self.p.title.text = title
        self.p.title.align = "center"
        show(self.p)
    
    #Makes a Categorical Graph
    def make_cat(self,title):
        if self.data == {}:
            self.make_data(title)

        self.z = figure(x_range=self.df_main['category_value'],plot_width=400, plot_height=600, tools="hover", toolbar_location=None, tooltips=[("$category_value" , "$value")])
        self.z.vbar(x = self.df_main['category_value'], top=(self.df_main['value'] / 2), width=0.5 )
        self.z.title.text = title

        show(self.z)

        
    
#demo = Graphs("earthquakes")
#demo3 = Graphs("earthquakes")
#demo2 = Graphs("../supermarkets")
#output_file("Graphs2.html")
#demo2.make_line("This be Pie", "Employees", "ID")
#demo.make_data('Pie')
#demo.get_average()
#demo.make_pie("This is a pie")
#demo3.make_cat("This is a Cat Chart")
#demo = Graphs("earthquakes")
#demo.make_table("This is the table for now")