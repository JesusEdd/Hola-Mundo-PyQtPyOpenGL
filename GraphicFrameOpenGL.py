from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
from PyQt5 import QtOpenGL # provides QGLWidget, QtWidgets,a special OpenGL QWidget)
import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality

from OpenGL.arrays import vbo
import numpy as np
import Figuras as fg

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(25, 25, 25)) # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST) # enable depth testing

        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(20.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix() # push the current matrix to the current stack

        gl.glTranslate(0.0, 0.0, -100.0)            # Profundidad en la que se presenta el objeto
        gl.glScale(5.0, 5.0, 5.0)                # Escala segun componente

        # Rotación (angulo,vector(x,y,z))
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)       # x
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)       # y
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)       # z
        #gl.glTranslate(-0.5, -0.5, -0.5)            # Traslacion según vector(x,y,z)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)
        #gl.glDrawArrays(gl.GL_QUADS,0,len(self.vertVBO))
        
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix() # restore the previous modelview matrix

    def initGeometry(self):
        self.cubeVtxArray = fg.Cvert
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,(1, -1)).astype(np.float32))
        self.vertVBO.bind()

        print(self.vertVBO)
        
        self.cubeClrArray = fg.Ccol
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
        (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = fg.Cindx

    def setRotX(self, val):
        self.rotX = val/np.pi

    def setRotY(self, val):
        self.rotY = val/np.pi

    def setRotZ(self, val):
        self.rotZ = val/np.pi
