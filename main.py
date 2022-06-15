from cgitb import text
from turtle import color, onclick
from kivy.app import App
from kivy.uix.button import Button
from  kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from skin_segmentation import get_segmented_skin
import cv2, string, random


def generate_id(N=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))

class TutorialApp(App):
    def build(self):
        layout = BoxLayout(orientation = 'vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.save_img = Button(text = "Click",pos_hint={'center_x': 0.5,'center_y':0.5},size_hint=(None,None))
        self.save_img.bind(on_press = self.take_picture)
        layout.add_widget(self.save_img)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video,1.0/30.0)
        return layout

    def load_video(self,*args):
        ret,frame = self.capture.read()
        self.image_frame = frame
        buffer = cv2.flip(frame,0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt ='bgr')
        texture.blit_buffer(buffer,colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture = texture

    def take_picture(self,*args):
        image_name = generate_id()+'.jpg'
        cv2.imwrite('assets/original/'+image_name,self.image_frame)
        cv2.imshow('Original Image',self.image_frame)
        segmented_img = get_segmented_skin(image_name)
        cv2.imwrite('assets/segmented/'+image_name,segmented_img)
        cv2.imshow('Segmented Image',segmented_img)

    

if __name__ == "__main__":
    TutorialApp().run()