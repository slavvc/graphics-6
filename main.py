from PIL import ImageTk
import tkinter as tk
import lib
import numpy as np

size = (200,400)

class Prog:
    def __init__(self, root):
        self.root = root

        self.polyhedron = lib.Polyhedron.Cube(lib.Point(0,0,0), 100)
        self.camera = lib.Camera.ortho()
        self.transform = lib.Transform.identity()

        self.camera_var = tk.IntVar()
        self.persp_k_var = tk.StringVar()
        self.iso_a_var = tk.StringVar()
        self.iso_b_var = tk.StringVar()
        self.object_var = tk.IntVar()
        self.radius_var = tk.StringVar()
        self.position_x_var = tk.StringVar()
        self.position_y_var = tk.StringVar()
        self.position_z_var = tk.StringVar()
        self.transform_mode_var = tk.IntVar()


        self.view = tk.Label(root, width=size[0], height=size[1])
        self.view.grid(row=0, column=0, rowspan=16)

        # Camera

        self.camera_var.trace('w', self.set_camera)
        tk.Label(root, text='Camera:').grid(row=0, column=1)
        tk.Radiobutton(
            root, text='ortho', variable=self.camera_var, value=0
        ).grid(row=1, column=2)

        tk.Radiobutton(
            root, text='persp', variable=self.camera_var, value=1
        ).grid(row=2, column=2)
        tk.Label(root, text='k:').grid(row=2, column=3)

        self.persp_k_var.trace('w', self.read_persp_k)
        tk.Entry(root, textvar=self.persp_k_var).grid(row=2, column=4)

        tk.Radiobutton(
            root, text='iso', variable=self.camera_var, value=2
        ).grid(row=3, column=2)
        tk.Label(root, text='a:').grid(row=3, column=3)

        self.iso_a_var.trace('w', self.read_iso_a_b)
        tk.Entry(root, textvar=self.iso_a_var).grid(row=3, column=4)
        tk.Label(root, text='b:').grid(row=3, column=5)

        self.iso_b_var.trace('w', self.read_iso_a_b)
        tk.Entry(root, textvar=self.iso_b_var).grid(row=3, column=6)

        # Object

        self.object_var.trace('w', self.set_object)
        tk.Label(root, text='Object:').grid(row=4, column=1)
        tk.Radiobutton(
            root, text='Cube', variable=self.object_var, value=0
        ).grid(row=5, column=2)
        tk.Radiobutton(
            root, text='Tetrahedron', variable=self.object_var, value=1
        ).grid(row=6, column=2)
        tk.Radiobutton(
            root, text='Octahedron', variable=self.object_var, value=2
        ).grid(row=7, column=2)


        self.radius_var.set(100)
        self.radius_var.trace('w', self.set_object)
        tk.Label(root, text='radius:').grid(row=4, column=3)
        tk.Entry(root, textvariable=self.radius_var).grid(row=4, column=4)

        # Position

        self.position_x_var.trace('w', self.set_object)
        self.position_y_var.trace('w', self.set_object)
        self.position_z_var.trace('w', self.set_object)
        self.position_x_var.set(0)
        self.position_y_var.set(20)
        self.position_z_var.set(0)
        tk.Label(root, text='Position:').grid(row=8, column=1)
        tk.Label(root, text='x:').grid(row=9, column=2)
        tk.Entry(root, textvariable=self.position_x_var).grid(row=9, column=3)
        tk.Label(root, text='y:').grid(row=9, column=4)
        tk.Entry(root, textvariable=self.position_y_var).grid(row=9, column=5)
        tk.Label(root, text='z:').grid(row=9, column=6)
        tk.Entry(root, textvariable=self.position_z_var).grid(row=9, column=7)

        # Transform
        tk.Label(root, text='Transform:').grid(row=10, column=1)

        self.transform_mode_var.trace('w', self.draw)
        tk.Radiobutton(
            root, text='Global', variable=self.transform_mode_var, value=0
        ).grid(row=10, column=2)
        tk.Radiobutton(
            root, text='Local', variable=self.transform_mode_var, value=1
        ).grid(row=10, column=3)
        # # Matrix
        tk.Label(root, text='Matrix:').grid(row=11, column=2)
        self.matrix_vars = []
        self.matrix_values = np.zeros((4,4))
        for i in range(4):
            self.matrix_vars.append([])
            for j in range(4):
                self.matrix_vars[i].append(tk.StringVar())
                self.matrix_values[i][j] = (1 if i==j else 0)
                tk.Entry(root, textvar=self.matrix_vars[i][j]).grid(
                    row=12+i, column=3+j
                )
                self.matrix_vars[i][j].set(1 if i==j else 0)
                self.matrix_vars[i][j].trace('w', self.read_matrix)

        self.draw()
    def draw(self, *args):
        if self.transform_mode_var.get() == 0:
            transformed = self.polyhedron.apply_transform(self.transform)
        else:
            transformed = self.polyhedron.apply_relative_transform(self.transform)
        self.im = self.camera.draw(size, transformed.points, transformed.sides)
        # self.im.show()
        self.pim = ImageTk.PhotoImage(self.im)
        self.view.configure(image=self.pim)

    def read_matrix(self, *args):
        try:
            for i in range(4):
                for j in range(4):
                    self.matrix_values[i][j] = float(self.matrix_vars[i][j].get())
            self.transform = lib.Transform(self.matrix_values)
        except:
            self.transform = lib.Transform.identity()
        self.draw()

    def read_persp_k(self, *args):
        try:
            self.persp_k = float(self.persp_k_var.get())
        except:
            # self.persp_k_var.set("error")
            self.persp_k = 0.1
        if self.camera_var.get() == 1:
            self.camera = lib.Camera.persp(self.persp_k)
        self.draw()

    def read_iso_a_b(self, *args):
        try:
            self.iso_a = float(self.iso_a_var.get())
            self.iso_b = float(self.iso_b_var.get())
        except:
            if self.camera_var.get() == 2:
                self.camera = lib.Camera.iso()
        else:
            if self.camera_var.get() == 2:
                self.camera = lib.Camera.iso(self.iso_a, self.iso_b)
        self.draw()

    def set_camera(self, *args):
        c = self.camera_var.get()
        if c == 0:
            self.camera = lib.Camera.ortho()
        elif c == 1:
            self.read_persp_k()
        elif c == 2:
            self.read_iso_a_b()
        self.draw()

    def set_object(self, *args):
        o = self.object_var.get()
        try:
            self.radius = float(self.radius_var.get())
        except:
            self.radius = 10
        self.read_position()
        if o == 0:
            self.polyhedron = lib.Polyhedron.Cube(self.position, self.radius)
        elif o == 1:
            self.polyhedron = lib.Polyhedron.Tetrahedron(self.position, self.radius)
        elif o == 2:
            self.polyhedron = lib.Polyhedron.Octahedron(self.position, self.radius)
        self.draw()

    def read_position(self, *args):
        try:
            self.position_x = float(self.position_x_var.get())
            self.position_y = float(self.position_y_var.get())
            self.position_z = float(self.position_z_var.get())
        except:
            self.position_x = 0
            self.position_y = 0
            self.position_z = 0
        self.position = lib.Point(
            self.position_x,
            self.position_y,
            self.position_z
        )

def main():
    root = tk.Tk()
    p=Prog(root)
    tk.mainloop()


if __name__ == '__main__':
    main()
