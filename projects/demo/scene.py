"""Reference scene showing the patterns used to build explainer videos here.

Render:
    ./render.sh projects/demo/scene.py DemoExplainer -ql
"""

from manim import *


class DemoExplainer(Scene):
    def construct(self):
        self.opening()
        self.equation_beat()
        self.graph_beat()
        self.closing()

    # Each "beat" is one idea from the script. Keeping them as separate methods
    # means a note like "redo the graph section" touches exactly one method.

    def opening(self):
        title = Text("The Derivative", font_size=72)
        subtitle = Text("a rate of change, made visual", font_size=32)
        subtitle.set_color(GREY_B)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=0.3 * DOWN))
        self.wait()
        self.play(FadeOut(VGroup(title, subtitle)))

    def equation_beat(self):
        # tex_to_color_map colors every matching substring at once.
        definition = MathTex(
            R"f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}",
            tex_to_color_map={"h": YELLOW, R"f'(x)": BLUE},
            font_size=60,
        )
        self.play(Write(definition))
        self.wait()

        # TransformMatchingTex morphs shared substrings instead of
        # cross-fading, which is what makes algebra steps read as continuous.
        slope = MathTex(
            R"f'(x) = \lim_{h \to 0} \frac{\Delta f}{h}",
            tex_to_color_map={"h": YELLOW, R"f'(x)": BLUE},
            font_size=60,
        )
        self.play(TransformMatchingTex(definition, slope, run_time=1.5))
        self.wait()
        self.play(FadeOut(slope))

    def graph_beat(self):
        axes = Axes(
            x_range=(-1, 4, 1),
            y_range=(-1, 5, 1),
            width=9,
            height=5.5,
            axis_config={"include_tip": True},
        )
        axes.add_coordinates(font_size=20)

        graph = axes.plot(lambda x: 0.4 * x**2, x_range=(-0.8, 3.4))
        graph.set_color(BLUE)
        graph_label = MathTex("f(x) = 0.4x^2", font_size=36)
        graph_label.set_color(BLUE)
        graph_label.next_to(axes.c2p(3.2, 4.1), RIGHT, buff=0.1)

        self.play(Create(axes), FadeIn(axes.coordinate_labels))
        self.play(Create(graph), Write(graph_label))
        self.wait()

        # A ValueTracker plus always_redraw is the standard way to drive a
        # continuously-moving element from a single number.
        x_tracker = ValueTracker(0.5)

        tangent = always_redraw(
            lambda: axes.get_tangent_line(
                x_tracker.get_value(), graph, length=4
            ).set_color(YELLOW)
        )
        dot = always_redraw(
            lambda: Dot(
                axes.i2gp(x_tracker.get_value(), graph), color=YELLOW, radius=0.06
            )
        )
        slope_readout = always_redraw(
            lambda: VGroup(
                MathTex(R"f'(x) = ", font_size=36),
                DecimalNumber(
                    axes.slope_of_tangent(x_tracker.get_value(), graph),
                    num_decimal_places=2,
                    font_size=36,
                ),
            )
            .arrange(RIGHT, buff=0.15)
            .set_color(YELLOW)
            .to_corner(UR)
        )

        self.play(Create(tangent), FadeIn(dot), FadeIn(slope_readout))
        self.play(x_tracker.animate.set_value(3.0), run_time=4, rate_func=smooth)
        self.wait()

        self.play(FadeOut(Group(*self.mobjects)))

    def closing(self):
        closing = Text("Slope of the tangent = the derivative", font_size=44)
        self.play(Write(closing))
        self.wait(1.5)
        self.play(FadeOut(closing))
