from manim import *
from scipy.integrate import solve_ivp
import numpy as np

def LorenzSystem(t, state, sigma = 10, rho = 28, beta = 8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def PointsForGoal(function, state0, time, dt = 0.01):
    solution = solve_ivp(function, t_span = (0, time), y0 = state0, t_eval = np.arange(0, time, dt))
    return solution.y.T

class LorenzAttractor(ThreeDScene):
    def construct(self):
      
        equations = MathTex(
            r"\dot{x} = \sigma(y - x)\\",
            r"\dot{y} = x(\rho - z) - y\\",
            r"\dot{z} = xy - \beta z",
            font_size=40
        ).to_corner(UL).set_stroke(width=1)
        
        
        equations.set_color_by_gradient("#00FFFF", "#FF00FF")
        self.add_fixed_in_frame_mobjects(equations)

        self.set_camera_orientation(phi = 75 * DEGREES, theta = - 45 * DEGREES, zoom = 0.8)
        axes = ThreeDAxes(
            x_range = (-50, 50, 5), y_range = (-50, 50, 5), z_range = (0, 50, 5),
            x_length = 16, y_length = 16, z_length = 5
        )
        self.add(axes)

        
        epsilon = 0.001
        states = [[10, 10, 10], [10, 10, 10 + epsilon]] 
        colors = ["#00FFFF", "#FF00FF"] 

        curves = VGroup()
        for i, state in enumerate(states):
            points = PointsForGoal(LorenzSystem, state, 30)
            curve = VMobject()
            m_points = [axes.c2p(p[0], p[1], p[2]) for p in points]
            curve.set_points_as_corners(m_points)
            curve.set_color(colors[i]) 
            curves.add(curve)
        
        
        dots = Group(*[Dot3D(color=color, radius = 0.05).scale(1.5) for color in colors])
        
        for dot, curve in zip(dots, curves):
            dot.move_to(curve.get_start())

        
        def update_dots(dots):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())
        
        dots.add_updater(update_dots)

        self.begin_ambient_camera_rotation(rate = 0.05)
        self.add(dots)
        self.play(*[Create(curve) for curve in curves], run_time = 15, rate_func=linear)
        self.wait(2)




