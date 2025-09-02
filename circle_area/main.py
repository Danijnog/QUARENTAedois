import numpy as np
from manim import *


class MyScene(Scene):
    """
    Classe para personalizar configurações do Manim.
    """

    def set_camera_background_color(self, color="#222125"):
        self.camera.background_color = color

    def small_pause(self, n=1):
        self.wait(n)

    def pause(self, n=2):
        self.wait(n)

    def medium_pause(self, n=4):
        self.wait(n)

    def long_pause(self, n=5):
        self.wait(n)


class CircleFormula(MyScene):
    """
    Classe principal da animação do vídeo.
    """

    def construct(self):
        self.set_camera_background_color()
        formula_circle = MathTex(r"Por \ que", r"\ \pi r^2?")
        formula_circle.to_edge(UP)

        self.play(FadeIn(formula_circle))
        self.long_pause()

        circle = Circle(color=WHITE)
        circle.scale(2.04)
        self.play(Create(circle))
        self.medium_pause()

        center = ORIGIN
        radius = 2
        n_values = [3, 6, 12, 24, 36]
        final_triangles = VGroup()
        initial_triangles = VGroup()
        self.play(FadeOut(formula_circle))
        self.pause()

        # Animação dos triângulos dentro do círculo
        for n in n_values:
            triangles = VGroup()
            for k in range(n):
                angle1 = 2 * PI * k / n
                angle2 = 2 * PI * (k + 1) / n
                p1 = radius * np.array([np.cos(angle1), np.sin(angle1), 0])
                p2 = radius * np.array([np.cos(angle2), np.sin(angle2), 0])
                tri = Polygon(center, p1, p2, fill_opacity=0.5, color=BLUE)
                triangles.add(tri)

            self.play(LaggedStart([Create(tri) for tri in triangles], lag_ratio=0.1))
            label = MathTex(rf"N_{{\triangle}} = {n}").to_corner(RIGHT)
            self.play(FadeIn(label))
            self.pause()

            self.play(FadeOut(triangles))
            self.play(FadeOut(label))

            if n == 6:
                initial_triangles = triangles
            if n == 36:
                final_triangles = triangles

        # Animação da transformação dos triângulos para a figura de "retângulo"
        circle.to_corner(LEFT)
        final_triangles.move_to(circle.get_center())
        initial_triangles.move_to(circle.get_center())
        self.play(Create(circle))
        self.small_pause()

        # Função auxiliar: pegar o ponto médio da base (médio de p1 e p2).
        def base_midpoint(poly: Polygon):
            v = poly.get_vertices()  # [centro, p1, p2]
            return (v[1] + v[2]) / 2

        n_triangles = [6, 36]
        total_items = len(n_triangles)
        for k, item in enumerate(n_triangles):
            triangles = initial_triangles if item == 6 else final_triangles
            self.play(Create(triangles))

            base_len = (
                2 * radius * np.sin(PI / item)
            )  # comprimento da corda (base de cada triângulo)
            half_per_row = item // 2  # triângulos por fileira

            row_width = half_per_row * base_len
            half_width = row_width / 2
            dtheta = TAU / item

            all_rect = VGroup()
            for i, tri in enumerate(triangles):
                t = tri.copy()

                # Ângulo médio do setor (para alinhar base horizontal)
                theta_mid = (i + 0.5) * dtheta

                # Rotaciona para que o bissetor fique vertical -> base horizontal
                t.rotate(PI / 2 - theta_mid, about_point=ORIGIN)

                # Fileiras alternadas: pares embaixo (apontando pra cima), 
                # ímpares em cima (apontando pra baixo)
                col = i // 2

                # centros x das bases: pares em posições ...,-1.5L,-0.5L,0.5L,1.5L,...; 
                # ímpares deslocadas por L/2
                x_even = -half_width + (col + 0.5) * base_len
                x_target = x_even if (i % 2 == 0) else (x_even + base_len / 2)
                y_target = -radius / 2 if (i % 2 == 0) else +radius / 2

                # Coloca a base exatamente na posição desejada
                bm = base_midpoint(t)
                shift_vec = np.array([x_target, y_target, 0]) - bm
                t.shift(shift_vec).shift(RIGHT * 2).shift(UP * 2)

                # Para a fileira de cima, queremos a base "virada" para baixo 
                # (apex para baixo)
                if i % 2 == 1:
                    t.rotate(PI).shift(DOWN * 2)

                all_rect.add(t)
            self.medium_pause()

            # Transformação: círculo -> “retângulo” alternado
            self.play(Transform(triangles, all_rect, run_time=2))
            self.medium_pause()
            if k < total_items - 1:
                self.play(FadeOut(all_rect), FadeOut(triangles))

        self.long_pause()

        # Colchetes
        brace_base = Brace(all_rect, direction=DOWN)
        label_base = MathTex(r"\frac{2 \pi r}{2} = ", "\pi r").next_to(brace_base, DOWN)
        add_label_base = (
            Tex("(Metade da circunferência do círculo)")
            .next_to(label_base, DOWN)
            .scale(0.7)
        )

        brace_height = Brace(all_rect, direction=RIGHT)
        label_height = MathTex(r"= r").next_to(brace_height, RIGHT)

        self.play(GrowFromCenter(brace_base), FadeIn(label_base))
        self.play(FadeIn(add_label_base))
        self.medium_pause()
        self.play(Indicate(label_base[1]))
        self.pause()
        self.play(GrowFromCenter(brace_height), FadeIn(label_height))
        self.medium_pause()
        self.play(Indicate(label_height))
        self.long_pause()

        # Formula final
        formula = MathTex(r"\text{Área} = (\pi r)\cdot r =", r"\pi r^2")
        formula.move_to(UP * 2)
        self.play(Write(formula), run_time=2)
        self.pause()

        self.play(Indicate(formula[1]))
        self.medium_pause()
