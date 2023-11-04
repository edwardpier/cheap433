import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Pulse:
    
    def __init__(self, time, duration):
        
        self.time = time
        self.duration = duration
        
    def get_time(self):
        return self.time
    
    def get_duration(self):
        return self.duration
    
    def durations_match(self, sub):
        
        diff = abs(self.duration - sub.duration)
        err = min(self.duration, sub.duration) * 0.1
        
        return diff < err
    
    def has_time(self, time):
        
        diff = abs(self.time - time)
        err = min(self.time, time)*0.1
        
        return diff < err
    
    
    

class PulseList:
    
    def __init__(self):
        
        self.pulses = []
        
    def is_empty(self):
        
        return len(self.pulses) == 0
    
    def add(self, time, duration):
        
        self.pulses.append(Pulse(time, duration))
        
    def find(self, sub):
        
        index = 0
        time0 = None
        
        intervals = []
        
        for pulse in self.pulses:
            
            if index == 0:
                if pulse.durations_match(sub):
                    time0 = pulse.get_time()
                    index += 1
                
                    
            else:
                if pulse.durations_match(sub) and
                   sub.has_time(pulse.get_time() - time0):
                    index += 1
                else:
                    index = 0
                    
            if index == len(sub):
                # found a match
                time1 = pulse.get_time()-time0
                intervals.append([time0, time1])
                
                index = 0
            
                 
                
                
        
    def read(self, filename):
        
        with open(filename) as f:
            
            start = None
            tick0 = None
            for line in f:
            
                fields = line.split()
                tick  = int(fields[0])
                level = int(fields[1])
                
                if tick0 is None:
                    tick0 = tick
                
                if level == 1:
                    # start of a pulse
                    start = tick
                    
                elif not      start is None:
                    # end of a pulse
                    duration = tick - start
                    
                    time = (start-tick0)
                    self.add(time, duration)

                    
class Transform:
    
    def __init__(self):
        
        self.interval = 100000
        self.tick0 = 0
        self.vsize = 10
        self.hscale = 700/self.interval
        
    def get_scaled_limits(self):
        
        x0 = 0
        x1 = int(self.interval * self.hscale)
        return x0, x1
        
    def copy(self):
        
        copy =  Transform()
        copy.interval = self.interval
        copy.tick0 = self.tick0
        copy.vsize = self.vsize
        copy.hscale = self.hscale
        
        return copy
    
        
    def time_to_pixels(self, time):
        
        time -= self.tick0
        row = time // self.interval
        remainder = time - row*self.interval
        
        i = int(remainder * self.hscale)
        j = int(row*self.vsize)

        return i, j
    
    def pixels_to_time(self, x, y):
        
        row = y//self.vsize
        time = self.tick0 + row*self.interval + x/self.hscale
        
        return time
        
    def duration_to_pixels(self, duration):
        
        width = int(duration*self.hscale)
        height = self.vsize
        
        return width, height
    
    def drag(self, x0, y0, x1, y1):
        
        trans = self.copy()
        trans.tick0 -= (x1-x0)/self.hscale
        
        return trans
    
    def stretch(self, x0, y0, x1, y1):
        
        trans = self.copy()
        trans.hscale *= x1/x0
        
        return trans
    
    def skew(self, x0, y0, x1, y1):
        
        trans = self.copy()
        trans.interval -= (x1-x0)/self.hscale/int(y0/trans.vsize)
        
        return trans
            
class SelectionModel:
    
    def __init__(self):
        
        self.intervals = []
        
    def add_interval(self, time0):
        
        new = [time0, time0]
        self.intervals.append(new)
        
        return new
        
    def is_selected(self, time):
        
        for interval in self.intervals:
            
            if time >= interval[0] and time <= interval[1]:
                return True
            
        return False
    
    def extract_from(self, pulses):
        
        sub = PulseList()
        
        for pulse in pulses.pulses:
            
            time = pulse.get_time()
            if self.is_selected(time):
                if sub.is_empty():
                    time0 = time
                    
                sub.add(time-time0, pulse.get_duration())
                
        return sub
                    
                
            

class Analyzer(QtWidgets.QWidget):
    
    def __init__(self, pulses):
        super().__init__()
        
        self.pulses = pulses
        
        self.selection = SelectionModel()
        self.transform = Transform()
        self.color = QtGui.QColor(0,0,0)
        self.selected_color = QtGui.QColor(255,0,0)
        self.mouse_mode = None
        self.new_selection = None

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)
        
        max_j = self.height()
        
        # draw boundary lines
        x0, x1 = self.transform.get_scaled_limits()
        painter.drawLine(x0, 0, x0, max_j)
        painter.drawLine(x1, 0, x1, max_j)
        
        for pulse in pulses.pulses:
            
            # unpack the pulse data
            time     = pulse.get_time()
            duration = pulse.get_duration()
            
            # where will it be on the screen?
            i, j = self.transform.time_to_pixels(time)
            if j>max_j:
                break
            
            width, height = self.transform.duration_to_pixels(duration)
            
            # check for selection
            if self.selection.is_selected(time):
                color = self.selected_color
            else:
                color = self.color
            
            # draw it
            painter.setPen(color)
            painter.drawRect(i, j, width, height)
            painter.fillRect(i, j, width, height, color)

            
    def mousePressEvent(self, event):
        
        self.mouse_x0 = event.x()
        self.mouse_y0 = event.y()
        self.transform0  = self.transform
        
        modifiers = event.modifiers()
        if modifiers & QtCore.Qt.ShiftModifier:
            self.mouse_mode = "stretch"
            
        elif modifiers & QtCore.Qt.ControlModifier:
            self.mouse_mode = "skew"
            
        elif modifiers & QtCore.Qt.AltModifier:
            self.mouse_mode = "select"
            
            time0 = self.transform.pixels_to_time(self.mouse_x0,
                                                  self.mouse_y0)
            
            self.new_selection = self.selection.add_interval(time0)
            
            
        else:
            self.mouse_mode = "drag"
        
        
    def mouseReleaseEvent(self, event):
        
        self.mouse_mode = None
        
        
    def mouseMoveEvent(self, event):
        
        x = event.x()
        y = event.y()
        
        if self.mouse_mode == 'drag':
            self.transform = self.transform0.drag(self.mouse_x0, 
                                                 self.mouse_y0, x, y)
        elif self.mouse_mode == 'stretch':
            self.transform = self.transform0.stretch(self.mouse_x0, 
                                                    self.mouse_y0, x, y)
        elif self.mouse_mode == 'skew':
            self.transform = self.transform0.skew(self.mouse_x0, 
                                                    self.mouse_y0, x, y)
        elif self.mouse_mode == 'select':
            time1 = self.transform.pixels_to_time(x, y)
            self.new_selection[1] = time1
            
            print(self.new_selection)
            
        
        if not self.mouse_mode is None:
            self.update()    

        

qapp = QtWidgets.QApplication(sys.argv)  

pulses = PulseList()
pulses.read('zz')

analyzer = Analyzer(pulses) 



analyzer.show()
qapp.exec_()
