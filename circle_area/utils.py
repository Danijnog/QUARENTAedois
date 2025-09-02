from manim import *


class BatteryRadio(VGroup):
    """
    Cria o personagem do canal.
    """

    def __init__(self, *args, **kwargs):
        (super().__init__(*args, **kwargs),)
        self.left_pupil = (None,)
        self.right_pupil = (None,)
        self.left_iris = (None,)
        self.right_iris = (None,)
        self.mouth = (None,)
        self.construct()

    def construct(self):
        # Face
        face = RoundedRectangle(
            width=2.5, height=1.5, corner_radius=0.15, color=BLUE, fill_opacity=0.9
        )

        # Criar olhos
        # Esclerótica
        left_eye = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(
            face.get_left() + RIGHT * 0.5 + UP * 0.25
        )
        right_eye = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(
            face.get_right() + LEFT * 0.5 + UP * 0.25
        )

        # Íris
        self.left_iris = Circle(radius=0.08, color=BLACK, fill_opacity=1).move_to(
            left_eye.get_center()
        )
        self.right_iris = Circle(radius=0.08, color=BLACK, fill_opacity=1).move_to(
            right_eye.get_center()
        )

        # Pupila
        self.left_pupil = Circle(radius=0.02, color=WHITE, fill_opacity=1).move_to(
            self.left_iris.get_left() + UP * 0.04 + RIGHT * 0.015
        )
        self.right_pupil = Circle(radius=0.02, color=WHITE, fill_opacity=1).move_to(
            self.right_iris.get_left() + UP * 0.04 + RIGHT * 0.015
        )

        left_highlight = Circle(radius=0.01, color=WHITE, fill_opacity=1).move_to(
            self.left_pupil.get_center() + UP * 0.01 + RIGHT * 0.01
        )
        right_highlight = Circle(radius=0.01, color=WHITE, fill_opacity=1).move_to(
            self.right_pupil.get_center() + UP * 0.01 + RIGHT * 0.01
        )

        # Mouth (smile)
        self.mouth = ArcBetweenPoints(
            face.get_left() + RIGHT + DOWN * 0.25,
            face.get_right() + LEFT + DOWN * 0.25,
            angle=TAU / 4,
            color=BLACK,
        )

        # Antenna
        antena = Line(start=face.get_top() + LEFT, end=face.get_top() + UP * 0.5)
        red_ball = Circle(radius=0.1, color=RED, fill_opacity=1).move_to(
            antena.get_end()
        )

        # Group everything
        full_emoji = VGroup(
            face,
            left_eye,
            right_eye,
            self.left_iris,
            self.right_iris,
            self.left_pupil,
            self.right_pupil,
            left_highlight,
            right_highlight,
            self.mouth,
            antena,
            red_ball,
        )
        self.add(full_emoji)

    def look_2_top_left(self):
        # Olho esquerdo completo
        left_eye = VGroup(self.left_iris, self.left_pupil)

        # Olho direito completo
        right_eye = VGroup(self.right_iris, self.right_pupil)

        return AnimationGroup(
            left_eye.animate.shift(UP * 0.05 + LEFT * 0.05),
            right_eye.animate.shift(UP * 0.05 + LEFT * 0.05),
            run_time=1,
        )

    def look_2_top_right(self):
        # Full left eye
        left_eye = VGroup(self.left_iris, self.left_pupil)

        # Full right eye
        right_eye = VGroup(self.right_iris, self.right_pupil)

        return AnimationGroup(
            left_eye.animate.shift(UP * 0.05 + RIGHT * 0.05),
            right_eye.animate.shift(UP * 0.05 + RIGHT * 0.05),
            run_time=1,
        )

    def change_mouth(self, new_mouth):
        # Return animation for changing the mouth
        return Transform(self.mouth, new_mouth)

    def wiggle_antenna(self):
        # Return animation for wiggling the antenna
        antena = self.submobjects[0][-2]  # Antenna line
        red_ball = self.submobjects[0][-1]  # Red ball

        return AnimationGroup(
            Rotate(antena, angle=0.3, about_point=antena.get_start()),
            Rotate(red_ball, angle=0.3, about_point=antena.get_start()),
            rate_func=smoothstep,
            run_time=0.5,
        )

    def blink(self):
        pass


class CustomSpeechBubble(VGroup):
    def __init__(self, direction, text=None, **kwargs):
        super().__init__(**kwargs)
        self.direction = direction
        if text:
            self.text = Tex(text)
        self.construct()

    def construct(self):
        # Criar o corpo do balão
        bubble_body = Ellipse(width=3, height=2, color=WHITE)
        second_bubble = Ellipse(width=1, height=0.5, color=WHITE)
        third_bubble = Ellipse(width=0.5, height=0.25, color=WHITE)

        # Agrupar as formas do balão
        if self.direction == "LEFT":
            second_bubble.move_to(bubble_body.get_bottom() + 2 * LEFT)
            third_bubble.move_to(second_bubble.get_bottom() + 0.75 * LEFT + 0.25 * DOWN)

        elif self.direction == "RIGHT":
            second_bubble.move_to(bubble_body.get_bottom() + 2 * RIGHT)
            third_bubble.move_to(
                second_bubble.get_bottom() + 0.75 * RIGHT + 0.25 * DOWN
            )

        else:
            raise Exception("Direção inválida. Use 'LEFT' ou 'RIGHT'.")

        # Criar o texto
        if hasattr(self, "text"):
            bubble_text = self.text
            bubble_text.scale_to_fit_width(bubble_body.width * 0.8)
            bubble_text.move_to(bubble_body.get_center())

        # Agrupar tudo
        full_bubble = VGroup(bubble_body, second_bubble, third_bubble, bubble_text)
        self.add(full_bubble)


class EmojiAnimate(Scene):
    def construct(self):
        emoji = BatteryRadio()

        self.play(Create(emoji))
        self.wait(1)

        self.play(emoji.look_2_top_left())
        self.wait(1)

        # Change mouth to sadness
        new_mouth = ArcBetweenPoints(
            emoji.mouth.get_start(), emoji.mouth.get_end(), angle=-TAU / 4, color=BLACK
        )
        self.play(emoji.change_mouth(new_mouth))
        self.wait(1)

        self.play(emoji.wiggle_antenna())
        self.wait(1)
        # self.wait(1)

    # self.wait(2)
