#!/usr/bin/env python2.2

## Stuff to integrate FloatCanvas into wxPython Demo
try:
    import Numeric
    def runTest(frame, nb, log):
        """
        This method is used by the wxPython Demo Framework for integrating
        this demo with the rest.
        """
        win = DrawFrame(NULL, -1, "FloatCanvas Drawing Window",wxDefaultPosition,wxSize(500,500))
        frame.otherWin = win
        win.Show(True)
except ImportError:
    def runTest(frame, nb, log):
        dlg = wxMessageDialog(frame, ('The FloatCanvas requires the Numeric module:\n'
                                      'You can get it at:\n'
                                      'http://sourceforge.net/projects/numpy'),
                          'Sorry', wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

from wxPython.lib import floatcanvas
from wxPython.wx  import *
import wxPython.lib.colourdb

ID_ABOUT_MENU = wxNewId()          
ID_EXIT_MENU  = wxNewId() 
ID_ZOOM_TO_FIT_MENU = wxNewId()
ID_DRAWTEST_MENU = wxNewId()
ID_LINETEST_MENU = wxNewId()
ID_DRAWMAP_MENU = wxNewId()
ID_DRAWMAP2_MENU = wxNewId()
ID_CLEAR_MENU = wxNewId()

colors = wxPython.lib.colourdb.getColourList()

LineStyles = floatcanvas.draw_object.LineStyleList.keys()

class DrawFrame(wxFrame):

    """

    A frame used for the FloatCanvas Demo
    
    """
    
    def __init__(self,parent, id,title,position,size):
        wxFrame.__init__(self,parent, id,title,position, size)
        
        ## Set up the MenuBar
        
        MenuBar = wxMenuBar()
        
        file_menu = wxMenu()
        file_menu.Append(ID_EXIT_MENU, "&Close","Close this frame")
        EVT_MENU(self, ID_EXIT_MENU,       self.OnQuit)
        MenuBar.Append(file_menu, "&File")
        
        draw_menu = wxMenu()
        draw_menu.Append(ID_DRAWTEST_MENU, "&Draw Test","Run a test of drawing random components")
        EVT_MENU(self, ID_DRAWTEST_MENU,self.DrawTest)
        draw_menu.Append(ID_LINETEST_MENU, "&Line Test","Run a test of drawing random lines")
        EVT_MENU(self, ID_LINETEST_MENU,self.LineTest)
        draw_menu.Append(ID_DRAWMAP_MENU, "Draw &Map","Run a test of drawing a map")
        EVT_MENU(self, ID_DRAWMAP_MENU,self.DrawMap)
        draw_menu.Append(ID_CLEAR_MENU, "&Clear","Clear the Canvas")
        EVT_MENU(self, ID_CLEAR_MENU,self.Clear)
        MenuBar.Append(draw_menu, "&Draw")
        
        
        view_menu = wxMenu()
        view_menu.Append(ID_ZOOM_TO_FIT_MENU, "Zoom to &Fit","Zoom to fit the window")
        EVT_MENU(self, ID_ZOOM_TO_FIT_MENU,self.ZoomToFit)
        MenuBar.Append(view_menu, "&View")
        
        help_menu = wxMenu()
        help_menu.Append(ID_ABOUT_MENU, "&About",
                                "More information About this program")
        EVT_MENU(self, ID_ABOUT_MENU,      self.OnAbout)
        MenuBar.Append(help_menu, "&Help")
        
        self.SetMenuBar(MenuBar)
        
        self.CreateStatusBar()
        self.SetStatusText("")
        
        EVT_CLOSE(self, self.OnCloseWindow)
        
        # Other event handlers:
        EVT_RIGHT_DOWN(self, self.RightButtonEvent)
        
        # Add the Canvas
        self.Canvas = floatcanvas.FloatCanvas(self,-1,(500,500),
                                  ProjectionFun = 'FlatEarth',
                                  Debug = 1,
                                  EnclosingFrame = self,
                                  BackgroundColor = "DARK SLATE BLUE",
                                  UseBackground = 0,
                                  UseToolbar = 1)
        self.Show(True)
        
        self.object_list = []
        
        return None
        
    def RightButtonEvent(self,event):
        print "Right Button has been clicked in DrawFrame"
        print "coords are: %i, %i"%(event.GetX(),event.GetY())
        event.Skip()
        
    def OnAbout(self, event):
        dlg = wxMessageDialog(self, "This is a small program to demonstrate\n"
                                                  "the use of the FloatCanvas\n",
                                                  "About Me", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def SetMode(self,event):
        for id in [ID_ZOOM_IN_BUTTON,ID_ZOOM_OUT_BUTTON,ID_MOVE_MODE_BUTTON]:
            self.ToolBar.ToggleTool(id,0)
        self.ToolBar.ToggleTool(event.GetId(),1)
        if event.GetId() == ID_ZOOM_IN_BUTTON:
            self.Canvas.SetGUIMode("ZoomIn")
        elif event.GetId() == ID_ZOOM_OUT_BUTTON:
            self.Canvas.SetGUIMode("ZoomOut")
        elif event.GetId() == ID_MOVE_MODE_BUTTON:
            self.Canvas.SetGUIMode("Move")
            
    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()
        
    def Clear(self,event = None):
        self.Canvas.RemoveObjects(self.object_list)
        self.object_list = []
        self.Canvas.Draw()
        
    def OnQuit(self,event):
        self.Close(True)
        
    def OnCloseWindow(self, event):
        self.Destroy()
        
    def DrawTest(self,event):
        wxGetApp().Yield()
        import random
        import RandomArray
        Range = (-10,10)
        
        Canvas = self.Canvas
        object_list = self.object_list
        
        ##		Random tests of everything:
        
        # Rectangles
        for i in range(5):
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            lw = random.randint(1,5)
            cf = random.randint(0,len(colors)-1)
            h = random.randint(1,5)
            w = random.randint(1,5)
            object_list.append(Canvas.AddRectangle(x,y,h,w,LineWidth = lw,FillColor = colors[cf]))
          
            # Ellipses
        for i in range(5):
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            lw = random.randint(1,5)
            cf = random.randint(0,len(colors)-1)
            h = random.randint(1,5)
            w = random.randint(1,5)
            object_list.append(Canvas.AddEllipse(x,y,h,w,LineWidth = lw,FillColor = colors[cf]))
          
            # Dots
        for i in range(5):
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            D = random.randint(1,50)
            lw = random.randint(1,5)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            object_list.append(Canvas.AddDot(x,y,D,LineWidth = lw,LineColor = colors[cl],FillColor = colors[cf]))
          
            # Circles
        for i in range(5):
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            D = random.randint(1,5)
            lw = random.randint(1,5)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            object_list.append(Canvas.AddCircle(x,y,D,LineWidth = lw,LineColor = colors[cl],FillColor = colors[cf]))
            self.object_list.append(self.Canvas.AddText("Circle # %i"%(i),x,y,Size = 12,BackGround = None,Position = "cc"))
          
            # Lines
        for i in range(5):
            points = []
            for j in range(random.randint(2,10)):
                point = (random.randint(Range[0],Range[1]),random.randint(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,10)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            self.object_list.append(self.Canvas.AddLine(points, LineWidth = lw, LineColor = colors[cl]))
          
            # Polygons
        for i in range(3):
            points = []
            for j in range(random.randint(2,6)):
                point = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,6)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            self.object_list.append(self.Canvas.AddPolygon(points,
                                                           LineWidth = lw,
                                                           LineColor = colors[cl],
                                                           FillColor = colors[cf],
                                                           FillStyle = 'Solid'))
            
            
        ## Pointset
        for i in range(4):
            points = []
            points = RandomArray.uniform(Range[0],Range[1],(100,2))
            cf = random.randint(0,len(colors)-1)
            D = random.randint(1,4)
            self.object_list.append(self.Canvas.AddPointSet(points, Color = colors[cf], Diameter = D))
        
        # Text
        String = "Some text"
        for i in range(10):
            ts = random.randint(10,40)
            cf = random.randint(0,len(colors)-1)
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            self.object_list.append(self.Canvas.AddText(String,x,y,Size = ts,ForeGround = colors[cf],Position = "cc"))
            
        self.Canvas.ZoomToBB()
        
    def DrawMap(self,event = None):
        wxGetApp().Yield()
        import os, time
    ## Test of Actual Map Data
        self.Clear()
        start = time.clock()
        Shorelines = Read_MapGen(os.path.join("data",'world.dat'),stats = 0)
        print "It took %f seconds to load %i shorelines"%(time.clock() - start,len(Shorelines) )
        start = time.clock()
        for segment in Shorelines:
            self.object_list.append(self.Canvas.AddLine(segment))
        print "It took %f seconds to add %i shorelines"%(time.clock() - start,len(Shorelines) )
        start = time.clock()
        self.Canvas.ZoomToBB()
        print "It took %f seconds to draw %i shorelines"%(time.clock() - start,len(Shorelines) )

##    def LineTest(self,event = None):
##        wxGetApp().Yield()
##        import os, time
##        import random
##        Range = (-10,10)
##    ## Test of drawing lots of lines
##        self.Clear()
##        start = time.clock()
##        linepoints = []
##        linecolors = []
##        linewidths = []
##        linestyles = []
##        for i in range(500):
##            points = (random.randint(Range[0],Range[1]),
##                     random.randint(Range[0],Range[1]))
##            linepoints.append(points)
##            points = (random.randint(Range[0],Range[1]),
##                     random.randint(Range[0],Range[1]))
##            linepoints.append(points)
##            linewidths.append(random.randint(1,10) )
##            linecolors.append(colors[random.randint(0,len(colors)-1) ])
##            linestyles.append(LineStyles[random.randint(0, len(LineStyles)-1)])

##        self.object_list.append(self.Canvas.AddLineSet(linepoints, LineWidths = linewidths, LineColors = linecolors, LineStyles = linestyles))
##        print "It took %f seconds to add %i lines"%(time.clock() - start,len(linepoints) )
##        start = time.clock()
##        self.Canvas.ZoomToBB()
##        print "It took %f seconds to draw %i lines"%(time.clock() - start,len(linepoints) )

    def LineTest(self,event = None):
        wxGetApp().Yield()
        import os, time
        import random
        Range = (-10,10)
    ## Test of drawing lots of lines
        self.Clear()
        start = time.clock()
        linepoints = []
        linecolors = []
        linewidths = []
        for i in range(2000):
            points = (random.randint(Range[0],Range[1]),
                     random.randint(Range[0],Range[1]),
                     random.randint(Range[0],Range[1]),
                     random.randint(Range[0],Range[1]))
            linepoints.append(points)
            linewidths.append(random.randint(1,10) )
            linecolors.append(random.randint(0,len(colors)-1) )
        for (points,color,width) in zip(linepoints,linecolors,linewidths):
            self.object_list.append(self.Canvas.AddLine((points[0:2],points[2:4]), LineWidth = width, LineColor = colors[color]))
        print "It took %f seconds to add %i lines"%(time.clock() - start,len(linepoints) )
        start = time.clock()
        self.Canvas.ZoomToBB()
        print "It took %f seconds to draw %i lines"%(time.clock() - start,len(linepoints) )

class DemoApp(wxApp):
    """
    How the demo works:
    
    Under the Draw menu, there are three options:
    
    *Draw Test: will put up a picture of a bunch of randomly generated
    objects, of each kind supported.
    
    *Draw Map: will draw a map of the world. Be patient, it is a big map,
    with a lot of data, and will take a while to load and draw (about 10 sec 
    on my 450Mhz PIII). Redraws take about 2 sec. This demonstrates how the
    performance is not very good for large drawings.
    
    *Clear: Clears the Canvas.
    
    Once you have a picture drawn, you can zoom in and out and move about
    the picture. There is a tool bar with three tools that can be
    selected. 
    
    The magnifying glass with the plus is the zoom in tool. Once selected,
    if you click the image, it will zoom in, centered on where you
    clicked. If you click and drag the mouse, you will get a rubber band
    box, and the image will zoom to fit that box when you release it.
    
    The magnifying glass with the minus is the zoom out tool. Once selected,
    if you click the image, it will zoom out, centered on where you
    clicked. (note that this takes a while when you are looking at the map,
    as it has a LOT of lines to be drawn. The image is double buffered, so
    you don't see the drawing in progress)
    
    The hand is the move tool. Once selected, if you click and drag on the
    image, it will move so that the part you clicked on ends up where you
    release the mouse. Nothing is changed while you are dragging. The
    drawing is too slow for that.
    
    I'd like the cursor to change as you change tools, but the stock
    wxCursors didn't include anything I liked, so I stuck with the
    pointer. Pleae let me know if you have any nice cursor images for me to
    use.
    
    
    Any bugs, comments, feedback, questions, and especially code are welcome:
    
    -Chris Barker
    
    Chris.Barker@noaa.gov

    """
    
    def OnInit(self):
        frame = DrawFrame(NULL, -1, "FloatCanvas Demo App",wxDefaultPosition,wxSize(700,700))

        self.SetTopWindow(frame)

        return True
            
def Read_MapGen(filename,stats = 0,AllLines=0):
    """
    This function reads a MapGen Format file, and
    returns a list of NumPy arrays with the line segments in them.
    
    Each NumPy array in the list is an NX2 array of Python Floats.
    
    The demo should have come with a file, "world.dat" that is the
    shorelines of the whole world, in MapGen format.
    
    """
    import string
    from Numeric import array
    file = open(filename,'rt')
    data = file.readlines()
    data = map(string.strip,data)
    
    Shorelines = []
    segment = []
    for line in data:
        if line:
            if line == "# -b": #New segment begining
                if segment: Shorelines.append(array(segment))
                segment = []
            else:
                segment.append(map(float,string.split(line)))
    if segment: Shorelines.append(array(segment))
    
    if stats:
        NumSegments = len(Shorelines)
        NumPoints = 0
        for segment in Shorelines:
            NumPoints = NumPoints + len(segment)
        AvgPoints = NumPoints / NumSegments
        print "Number of Segments: ", NumSegments
        print "Average Number of Points per segment: ",AvgPoints
    if AllLines:
        Lines = []
        for segment in Shorelines:
            Lines.append(segment[0])
            for point in segment[1:-1]:
                Lines.append(point)
                Lines.append(point)
            Lines.append(segment[-1])
        #print Shorelines
        #for point in Lines: print point
        return Lines
    else:
        return Shorelines

## for the wxPython demo:
overview = floatcanvas.FloatCanvas.__doc__
  
if __name__ == "__main__":
    app = DemoApp(0)
    app.MainLoop()



