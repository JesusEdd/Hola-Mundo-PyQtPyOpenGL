from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

import sys
import ctypes                   #Permite acceder a Dimensiones del escritorio

from GraphicFrameOpenGL import GLWidget                 #Clase de archivo externo que contiene el OpenGLWidget

class Ventana(QMainWindow):                             #Clase heredada de QMainWindow
                                                        #Constructor de Ventanas
    def __init__(self):                                 #Metodo Constructor de la clase
        QMainWindow.__init__(self)                      #Iniciar Objeto QMainWindow

                                                        
        loadUi("Interface.ui",self)                     #Carga el archivo .ui en objeto
        self.setWindowTitle("Robot Joint Simulator")    #Título de la ventana

        #Fijar el tamaño de la ventana
        self.setMinimumSize(830,630)                    #Tamaño mínimo
        self.setMaximumSize(830,630)                    #Tamaño maximo

        #Mover la ventana y centrarla en escritorio
        resolucion=ctypes.windll.user32
        res_anch=resolucion.GetSystemMetrics(0)         # Extrae dimensiones 
        res_alto=resolucion.GetSystemMetrics(1)         #  de la pantalla
        left=int((res_anch/2)-(self.frameSize().width()/2))
        top=int((res_alto/2)-(self.frameSize().height()/2))
        self.move(left,top)                             #Posicion de Ventana

        qfont=QFont("Arial",12,QFont.Bold)              #Asignar fuente
        self.setFont(qfont)

    # Widgets ---------------------------------------------------------
        #OpenGLWidget --------------------------------------------------
        self.glWidget = GLWidget(self)          
        self.glWidget.setGeometry(260,50,480,480)       #Dibujar el OpenGL Widget en pantalla

        timer = QTimer(self)
        timer.setInterval(10)                           #Intervalo en milisegundos
        timer.timeout.connect(self.glWidget.updateGL)   #Evento timeout llama al Método updateGL
        timer.start()                                   #Timer se reinicia para redibujar

        #Sliders-------------------------------------------------------
        
        self.J1_ctl.setValue(0)
        self.J1_ctl.valueChanged.connect(self.getValueJ1)
        self.J1_label.setText(str(self.J1_ctl.value())+" °")

        self.J2_ctl.setValue(0)
        self.J2_label.setText(str(self.J2_ctl.value())+" °")
        self.J2_ctl.valueChanged.connect(self.getValueJ2)

        self.J3_ctl.setValue(0)
        self.J3_label.setText(str(self.J3_ctl.value())+" °")
        self.J3_ctl.valueChanged.connect(self.getValueJ3)

        self.SL_RotX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))
        self.SL_RotY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))
        self.SL_RotZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        
        # PusButtons ----------------------------------------------
        self.RestartButton.clicked.connect(self.restartValues)

    # Metodos -----------------------------------------------------------
        
    # Joint-Control de sliders Methods
    def getValueJ1(self):
        value1=self.J1_ctl.value()
        self.J1_label.setText(str(value1)+" °")
        
    def getValueJ2(self):
        value2=self.J2_ctl.value()
        self.J2_label.setText(str(value2)+" °")

    def getValueJ3(self):
        value3=self.J3_ctl.value()
        self.J3_label.setText(str(value3)+" °")
        
    # Reiniciar Sliders
    def restartValues(self):
        if self.RestartButton.clicked:
            self.J1_ctl.setValue(0)
            self.J2_ctl.setValue(0)
            self.J3_ctl.setValue(0)
            self.SL_RotX.setValue(0)
            self.SL_RotY.setValue(0)
            self.SL_RotZ.setValue(0)
    
    # Asignar un valor a label
    def showEvent(self,event):
        self.WelcomeLabel.setText("¡¡¡¡Bienvenido!!!!")

    # Genera un cuadro de dialogo a la salida de la aplicacion
    def closeEvent(self,event):
        resultado=QMessageBox.question(self,"Salir...",
        "¿Seguro que quieres salir de la aplicacion",
        QMessageBox.Yes | QMessageBox.No)

        if resultado==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
# Final de la clase Ventana(QMainWindow)

app=QApplication(sys.argv)              #Instancia para iniciar aplicación
_ventana=Ventana()                      #Crear un objeto de la clase Ventana
_ventana.show()                         #Mostrar la ventana
app.exec_()                             #Ejecutar la aplicacion



