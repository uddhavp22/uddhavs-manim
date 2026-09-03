"""Chapter B.9 — which frequencies are useful for a finite batch.

B08 established that the complete population characteristic function is
unique. A finite batch only estimates that curve, so this scene compares real
shape separation with ordinary resampling variation. The result motivates a
smooth taper across frequency rather than a data-chosen hard window.
"""

import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.anim import lagged_map
from common import data, layout
from common.beat import ActScene
from common.fingerprint import CharacteristicFunctionPlot
from common.palette import CLOUD, COLLAPSE, EMPIRICAL, INK, MUTED, TARGET
from common import type as ty
from common.wrap import ecf, gaussian_cf


T_MAX = layout.FREQUENCY_T_MAX
GRID = np.linspace(0.0, T_MAX, 700)
N_SAMPLES = 40
GAUSS = data.gaussian_1d(N_SAMPLES)
BIMODAL = data.bimodal_1d(N_SAMPLES)


class B09(ActScene):
    chain_link = "characteristic functions"

    def construct(self):
        self.plot = CharacteristicFunctionPlot()
        self.axes = self.plot.axes
        self.plot.mount(self)

        self.gaussian_values = ecf(GAUSS, GRID).real
        self.bimodal_values = ecf(BIMODAL, GRID).real

        self.compare_shapes()
        self.show_sampling_noise()
        self.motivate_weight()

    # ------------------------------------------------------------------
    def compare_shapes(self):
        """Probe the same two curves at a weak and a revealing frequency."""
        legend = VGroup(
            ty.label("bell-shaped batch", color=EMPIRICAL),
            ty.label("two clumps", color=COLLAPSE),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        legend.move_to(self.axes.c2p(5.25, 0.82))

        frequency = ValueTracker(0.3)
        gaussian_curve = self.plot.curve(
            GRID, self.gaussian_values, EMPIRICAL,
        )
        bimodal_curve = self.plot.curve(
            GRID, self.bimodal_values, COLLAPSE,
        )
        probe = self._comparison_probe(frequency)
        readout = self._comparison_readout(frequency)

        with self.voiceover(
            text="If we place the characteristic functions of our first two "
                 "batches together, <bookmark mark='gap'/>their gap at t equals "
                 "point three is close to zero."
        ) as tracker:
            self.play(
                Create(gaussian_curve),
                Create(bimodal_curve),
                FadeIn(legend),
                run_time=max(1.6, tracker.time_until_bookmark("gap")),
                rate_func=linear,
            )
            self.wait_until_bookmark("gap")
            self.add(probe)
            self.play(FadeIn(readout), run_time=0.35)
            self.across(
                tracker,
                Indicate(
                    readout[1], color=INK, scale_factor=1.025,
                ),
                floor=0.8,
            )
        self.inspect(0.65)

        with self.voiceover(
            text="At t equals three, the difference in their shapes leaves a "
                 "much larger gap."
        ) as tracker:
            self.across(
                tracker,
                frequency.animate.set_value(3.0),
                floor=2.0,
                rate_func=linear,
            )
        self.inspect(0.85)

        self.frequency = frequency
        self.gaussian_curve = gaussian_curve
        self.bimodal_curve = bimodal_curve
        self.comparison_probe = probe
        self.comparison_readout = readout
        self.legend = legend

    def _values_at(self, frequency):
        t = frequency.get_value()
        gaussian = float(np.interp(t, GRID, self.gaussian_values))
        bimodal = float(np.interp(t, GRID, self.bimodal_values))
        return t, gaussian, bimodal

    def _comparison_probe(self, frequency):
        return VGroup(
            self._moving_gap_dots(frequency),
            self._moving_gap_endpoints(frequency),
        )

    def _comparison_readout(self, frequency):
        t_number = DecimalNumber(
            0.0, num_decimal_places=2, font_size=ty.READOUT, color=INK,
        )
        gap_number = DecimalNumber(
            0.0,
            num_decimal_places=4,
            font_size=ty.READOUT,
            color=INK,
        )
        t_number.add_updater(
            lambda number: number.set_value(frequency.get_value())
        )
        gap_number.add_updater(
            lambda number: number.set_value(abs(
                self._values_at(frequency)[1] - self._values_at(frequency)[2]
            ))
        )
        t_group = VGroup(
            ty.maths("t=", size=ty.READOUT, color=INK), t_number,
        ).arrange(RIGHT, buff=0.08)
        gap_group = VGroup(
            ty.words("vertical gap", size=ty.LABEL, color=MUTED),
            ty.maths("=", size=ty.READOUT, color=MUTED),
            gap_number,
        ).arrange(RIGHT, buff=0.10)
        readout = VGroup(t_group, gap_group).arrange(RIGHT, buff=0.65)
        readout.move_to(np.array([0.0, 2.65, 0.0]))
        return readout

    def _t_readout(self, frequency):
        number = DecimalNumber(
            frequency.get_value(),
            num_decimal_places=2,
            font_size=ty.READOUT,
            color=INK,
        )
        number.add_updater(
            lambda mob: mob.set_value(frequency.get_value())
        )
        readout = VGroup(
            ty.maths("t=", size=ty.READOUT, color=INK), number,
        ).arrange(RIGHT, buff=0.08)
        readout.move_to(np.array([0.0, 2.65, 0.0]))
        return readout

    # ------------------------------------------------------------------
    def show_sampling_noise(self):
        """Repeat one population experiment with several finite batches."""
        rng = np.random.default_rng(20260806)
        estimate_values = [
            ecf(rng.standard_normal(N_SAMPLES), GRID).real
            for _ in range(14)
        ]
        estimates = VGroup(*(
            self.plot.curve(
                GRID, values, CLOUD, width=2.2, opacity=0.52,
            )
            for values in estimate_values
        ))
        population = self.plot.curve(
            GRID, gaussian_cf(GRID), TARGET, width=5,
        )

        with self.voiceover(
            text="But larger t is not automatically better. Suppose we take "
                 "fresh samples from the same Gaussian. Each batch gives a "
                 "slightly different estimate of the same curve."
        ) as tracker:
            self.freeze(
                self.comparison_probe,
                self.comparison_readout,
            )
            self.play(
                FadeOut(VGroup(
                    self.gaussian_curve,
                    self.bimodal_curve,
                    self.comparison_probe,
                    self.comparison_readout,
                    self.legend,
                )),
                run_time=0.55,
            )
            self.play(Create(population), run_time=0.8)
            self.across(
                tracker,
                lagged_map(Create, estimates, lag_ratio=0.07),
                floor=2.5,
            )

        noise_frequency = ValueTracker(3.4)
        noise_t_readout = self._t_readout(noise_frequency)

        def current_noise_probe():
            t = noise_frequency.get_value()
            guide = DashedLine(
                self.axes.c2p(t, -0.55),
                self.axes.c2p(t, 0.55),
                dash_length=0.07,
            ).set_stroke(MUTED, 1.5)
            sample_dots = VGroup(*(
                Dot(
                    self.axes.c2p(t, np.interp(t, GRID, values)),
                    radius=0.045,
                    color=CLOUD,
                )
                for values in estimate_values
            ))
            population_dot = Dot(
                self.axes.c2p(t, gaussian_cf(t)),
                radius=0.06,
                color=TARGET,
            )
            return VGroup(guide, sample_dots, population_dot)

        noise_probe = always_redraw(current_noise_probe)

        with self.voiceover(
            text="Near the tail, those estimates spread apart even though the "
                 "distribution has not changed. That variation is sampling "
                 "noise, so it need not represent real structure."
        ) as tracker:
            self.add(noise_probe)
            self.play(FadeIn(noise_t_readout), run_time=0.35)
            self.across(
                tracker,
                noise_frequency.animate.set_value(6.15),
                floor=1.5,
                rate_func=linear,
            )
        self.inspect(0.85)

        self.estimates = estimates
        self.estimate_values = estimate_values
        self.population = population
        self.noise_probe = noise_probe
        self.noise_t_readout = noise_t_readout

    # ------------------------------------------------------------------
    def motivate_weight(self):
        """Compare shape separation with finite-sample variation.

        The blue band is estimated from repeated Gaussian batches; the red
        curve comes from the two-clump batch.  The conclusion is qualitative:
        retain the whole family of frequencies, while letting the influence
        taper before high-frequency sampling variation dominates.
        """
        sampling_variation = np.std(
            np.asarray(self.estimate_values), axis=0,
        )
        bell_curve = self.plot.curve(
            GRID, self.gaussian_values, EMPIRICAL, width=4,
        ).set_z_index(2)
        clumps_curve = self.plot.curve(
            GRID, self.bimodal_values, COLLAPSE, width=4,
        ).set_z_index(2)
        variation_band = self._variation_band(
            self.gaussian_values, sampling_variation,
        )

        def line_key(color, label):
            swatch = Line(0.20 * LEFT, 0.20 * RIGHT).set_stroke(color, 4)
            return VGroup(
                swatch,
                ty.label(label, color=INK),
            ).arrange(RIGHT, buff=0.12)

        legend = VGroup(
            line_key(EMPIRICAL, "bell-shaped batch"),
            line_key(COLLAPSE, "two-clump batch"),
        ).arrange(RIGHT, buff=0.55)
        legend.move_to(np.array([-1.3, 2.65, 0.0]))

        band_key = VGroup(
            Rectangle(
                width=0.42,
                height=0.18,
                stroke_width=1.5,
                stroke_color=CLOUD,
                fill_color=CLOUD,
                fill_opacity=0.18,
            ),
            ty.label("same-Gaussian variation", color=INK),
        ).arrange(RIGHT, buff=0.12)
        band_key.move_to(np.array([3.6, 2.65, 0.0]))

        with self.voiceover(
            text="Condense those Gaussian resamples into this "
                 "<bookmark mark='band'/>blue band. Its width records the "
                 "variation produced by one unchanged distribution. The "
                 "<bookmark mark='clumps'/>red curve is the two-clump batch."
        ) as tracker:
            self.freeze(self.noise_probe, self.noise_t_readout)
            self.play(
                FadeOut(VGroup(
                    self.noise_probe,
                    self.noise_t_readout,
                    self.estimates,
                    self.population,
                )),
                run_time=0.7,
            )
            self.wait_until_bookmark("band")
            self.play(
                FadeIn(variation_band),
                Create(bell_curve),
                FadeIn(band_key),
                run_time=0.9,
            )
            self.wait_until_bookmark("clumps")
            self.play(
                Create(clumps_curve),
                FadeIn(legend),
                run_time=0.9,
            )
            self.across(tracker, Wait(0.1), floor=0.35)

        probe_frequency = ValueTracker(0.3)
        probe = self._window_probe(probe_frequency)
        probe_readout = self._t_readout(probe_frequency)
        probe_readout.move_to(np.array([0.0, 2.10, 0.0]))

        with self.voiceover(
            text="Near zero, every characteristic function is anchored at "
                 "one, so the gap begins small. <bookmark mark='middle'/>"
                 "Through the middle frequencies, the two-clump curve moves "
                 "well beyond ordinary resampling variation. "
                 "<bookmark mark='tail'/>Farther out, that variation becomes "
                 "a larger part of what we see."
        ) as tracker:
            self.add(probe)
            self.play(FadeIn(probe_readout), run_time=0.35)
            self.wait_until_bookmark("middle")
            self.play(probe_frequency.animate.set_value(3.0), run_time=2.0,
                      rate_func=smooth)
            self.wait_until_bookmark("tail")
            self.across(tracker,
                        probe_frequency.animate.set_value(5.8), floor=2.0,
                        rate_func=smooth)

        self.freeze(probe, probe_readout)

        influence_axes = Axes(
            x_range=(0, T_MAX, 1), y_range=(0, 1.05, 0.5),
            x_length=5.4, y_length=1.15,
            axis_config={"include_tip": False, "stroke_width": 1.4},
        ).move_to(np.array([0.0, -2.30, 0.0]))
        taper = VMobject().set_stroke(TARGET, 3)
        taper.set_points_as_corners([
            influence_axes.c2p(t, np.exp(-0.5 * t * t)) for t in GRID
        ])
        taper_label = ty.label("frequency influence", color=TARGET)
        taper_label.next_to(influence_axes, UP, buff=0.12)

        with self.voiceover(
            text="So the score should keep every frequency, while letting "
                 "their influence fade smoothly into the noisy tail. "
                 "<bookmark mark='taper'/>This taper is the idea we will put "
                 "into the final formula."
        ) as tracker:
            self.play(FadeOut(VGroup(probe, probe_readout)), run_time=0.4)
            self.wait_until_bookmark("taper")
            self.across(tracker, Create(influence_axes), Create(taper),
                        FadeIn(taper_label), floor=1.4)

        with self.voiceover(
            text="The standard Gaussian now supplies the reference curve that "
                 "each batch will be compared with."
        ) as tracker:
            self.across(
                tracker,
                FadeOut(VGroup(
                    bell_curve,
                    clumps_curve,
                    variation_band,
                    legend,
                    band_key,
                    influence_axes,
                    taper,
                    taper_label,
                )),
                floor=1.0,
            )

        self.settle_frame()
        # Exact last-frame handoff to B10: shared bare axes and labels.

    def _variation_band(self, centre, half_width):
        """A quiet uncertainty band around one representative batch curve."""
        upper = [
            self.axes.c2p(t, value + spread)
            for t, value, spread in zip(GRID, centre, half_width)
        ]
        lower = [
            self.axes.c2p(t, value - spread)
            for t, value, spread in zip(GRID, centre, half_width)
        ]
        band = VMobject()
        band.set_points_as_corners(upper + list(reversed(lower)) + [upper[0]])
        band.set_fill(CLOUD, opacity=0.16)
        band.set_stroke(CLOUD, width=1.2, opacity=0.35)
        band.set_z_index(-1)
        return band

    def _window_probe(self, frequency):
        return VGroup(
            self._moving_gap_dots(frequency),
            self._moving_gap_endpoints(frequency),
        )

    def _moving_gap_dots(self, frequency):
        """A fixed dot family whose positions follow one frequency tracker.

        Rebuilding a ``DashedLine`` changes its dash count as the gap length
        changes, which makes the segment flicker.  Keeping the same dots and
        only updating their positions gives the sweep continuous identity.
        """
        gap_dots = VGroup()
        for alpha in np.linspace(0.08, 0.92, 13):
            dot = Dot(radius=0.017, color=INK)

            def follow_gap(mob, blend=alpha):
                _, gaussian, bimodal = self._values_at(frequency)
                start = self.axes.c2p(frequency.get_value(), gaussian)
                end = self.axes.c2p(frequency.get_value(), bimodal)
                length = np.linalg.norm(end - start)
                mob.move_to((1.0 - blend) * start + blend * end)
                mob.set_opacity(min(1.0, length / 0.16))

            dot.add_updater(follow_gap, call_updater=True)
            gap_dots.add(dot)
        gap_dots.set_z_index(4)
        return gap_dots

    def _moving_gap_endpoints(self, frequency):
        gaussian_dot = Dot(radius=0.05, color=EMPIRICAL)
        bimodal_dot = Dot(radius=0.05, color=COLLAPSE)
        gaussian_dot.add_updater(
            lambda mob: mob.move_to(self.axes.c2p(
                frequency.get_value(), self._values_at(frequency)[1],
            )),
            call_updater=True,
        )
        bimodal_dot.add_updater(
            lambda mob: mob.move_to(self.axes.c2p(
                frequency.get_value(), self._values_at(frequency)[2],
            )),
            call_updater=True,
        )
        return VGroup(gaussian_dot, bimodal_dot).set_z_index(5)
