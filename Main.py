#Boa:Frame:Frame1
from __future__ import division
from Settings import Settings
import wx
import Preferences
import cv2
import ltools.image
import ltools.convert
from PIL import Image
import facedetect
import numpy
from ltools import tracker

#t = cv2.VideoCapture(0)



def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON_SETTINGS, wxID_FRAME1PANEL_CAMERA,
 wxID_FRAME1PANEL_MAIN,
] = [wx.NewId() for _init_ctrls in range(4)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(552, 349), size=wx.Size(431, 234),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Camera Mouse')
        self.SetClientSize(wx.Size(415, 196))
        self.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
        self.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)

        self.panel_main = wx.Panel(id=wxID_FRAME1PANEL_MAIN, name=u'panel_main',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(415, 196),
              style=wx.TAB_TRAVERSAL)

        self.panel_camera = wx.Panel(id=wxID_FRAME1PANEL_CAMERA,
              name=u'panel_camera', parent=self.panel_main, pos=wx.Point(16,
              16), size=wx.Size(200, 160), style=wx.TAB_TRAVERSAL)
        self.panel_camera.SetBackgroundColour(wx.Colour(240, 240, 200))

        self.button_settings = wx.Button(id=wxID_FRAME1BUTTON_SETTINGS,
              label=u'&Settings..', name=u'button_settings',
              parent=self.panel_main, pos=wx.Point(224, 152), size=wx.Size(75,
              23), style=0)
        self.button_settings.Bind(wx.EVT_BUTTON, self.OnButton_settingsButton,
              id=wxID_FRAME1BUTTON_SETTINGS)

    def __init__(self, parent):
        self._init_ctrls(parent)



        self.settings = Settings(self)

        self.preferences = Preferences.create(self)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Timer = wx.Timer(self)
        self.Timer_alt = wx.Timer(self) #used to force update when eg clicking on the title bar (which stops on_idle)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.Timer)
        self.Bind(wx.EVT_TIMER, self.on_idle, self.Timer_alt)
        self.Timer_alt.Start(200)
        self.Timer.Start(30) # required to trigger the on_idle..
        self.faceDector = facedetect.FaceDetect()
        self.test_title = 'ahooi daar'

        self.tracker = tracker.LKTracker()
        self.tracker.display_window = 1

#        self.camera = self.settings.face_tracking_camera
        print 'done'


    def draw_rects(self, img, rects, color):

       # rects[:, 2:] += rects[:, :2]  #transforsms [x, y, w, h] to [x, y, x+w, y+h]
        for x1, y1, w, h in rects:
            cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), color, 1)

    def on_idle(self, event):

        ret, frame = self.camera.read()
        dc = wx.ClientDC(self.panel_camera)  #320x240
        h, w, d = frame.shape
        frame = cv2.resize(frame, (200, int(200 / w * h)))
        frame = cv2.flip(frame, 1)

        frame_color = numpy.copy(frame)
#        self.tracker.update(frame_color)
        h, w, d = frame.shape


#        frame = ltools.image.convert_to_grayscale(frame)
#        frame = cv2.equalizeHist(frame)
        self.faceDector.update(frame_color)

        if len(self.faceDector.face_rect):
#            print self.faceDector.tempval
            if self.faceDector._diffsize < 0.1:
                self.draw_rects(frame_color, [self.faceDector.face_rect], (255, 0, 100))
            else:
                self.draw_rects(frame_color, [self.faceDector.face_rect], (155, 100, 100))

        if self.faceDector.ready:
            self.draw_rects(frame_color, [self.faceDector.face_rect_raw], (255, 0, 000))
#        return
        #print len(self.faceDector._face_sizes_list)
#        print self.faceDector.face_rect
        if 0 and len(self.faceDector.face_rect):
            self.draw_rects(frame_color, [self.faceDector.face_rect], (255, 0, 0))
            x, y = self.faceDector.zero_pos
            self.draw_rects(frame_color, [[x - 2, y - 2, x + 2, y + 2]], (255, 0, 0))
#            print self.faceDector.face_rect
            x1, y1, x2, y2 = self.faceDector.face_rect



#            face_img = frame[y1:y2, x1:x2]
#            eyes = self.faceDector.detect_eyes_with_cascade(face_img)
#            if (eyes != None and len(eyes)):
#                self.draw_rects(frame_color, eyes + [x1, y1, x1, y1], (255, 110, 100));
#
#            self.faceDector.detect_nose_with_cascade(face_img)
#
#            self.draw_rects(frame_color, [self.faceDector.nose_rect + [x1, y1, x1, y1]], (200, 110, 100));
#            print [self.faceDector.nose_rect + [x1, y1, x1, y1]]
#            w = x2 - x1
#            h = y2 - y1
#
#            if not self.tracker.track_rectangle or abs(self.tracker.get_center()[0] - (x1 + w // 2)) > 15:
#                self.tracker.reset([x1 + w // 3 , y1 + w // 3 + (w // 8) , w // 3 , w // 3 ])
#            else:
#                x, y = self.tracker.get_center()
#                self.draw_rects(frame_color, [[x - (w) // 2, y - (h) // 2 - (w // 8), x + (w) // 2, y + (h) // 2 - (w // 8)]], (255, 255, 0))
#
#                self.draw_rects(frame_color, [self.faceDector.nose_rect + [x - (w) // 2, y - (h) // 2 - (w // 8), x - (w) // 2, y - (h) // 2 - (w // 8)]], (100, 110, 100));

          #  self.draw_rects(frame_color, [[x1 + w // 3 , y1 + w // 3 , x2 - w // 3, y2 - w // 3]], (255, 110, 0))


        dc.DrawBitmap(ltools.convert.numpyToBitmap(frame_color), 0, 0, False)
        #print 'idle'

    def OnTimer(self, event):
        pass


    def OnButton_settingsButton(self, event):
        self.preferences.Show()
        event.Skip()
