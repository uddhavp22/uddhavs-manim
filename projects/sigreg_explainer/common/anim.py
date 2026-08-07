"""Animation helpers that paper over Manim Community's sharper edges.

Currently one: a `LaggedStartMap` that means what it said under manimgl.
"""

from __future__ import annotations

from typing import Any

from manim import LaggedStartMap, Mobject
from manim.animation.animation import Animation


def _one(mob: Mobject) -> tuple[Mobject]:
    return (mob,)


def lagged_map(animation_class: type[Animation], group: Mobject,
               **kwargs: Any) -> LaggedStartMap:
    """One animation per direct submobject of `group`, staggered.

    Use this instead of `LaggedStartMap` directly. Manim Community's version
    builds its animations as `animation_class(*arg_creator(submob))`, and the
    default `arg_creator` is the identity -- so it unpacks each submobject as an
    argument *list*. `Mobject.__iter__` yields the mobject itself followed by its
    children, which means an `Arrow` (a shaft with a tip submobject) expands to
    two arguments, and the tip lands in the animation's second positional
    parameter:

        LaggedStartMap(GrowArrow, arrows)  ->  GrowArrow(arrow, tip)
                                               #             ^ point_color

    Nothing raises at construction. It raises inside `begin()`, several frames of
    narration later, as `AttributeError: ArrowTriangleFilledTip object has no
    attribute 'hex'` -- because the tip is being parsed as a colour. That is what
    it did in b01's average beat.

    The same unpacking silently mis-binds `Indicate(mob, scale_factor, color)`
    and `Create(mob, lag_ratio, introducer)`. It happens to be harmless for
    `FadeIn(*mobjects)`, which is variadic, but only by luck -- and there it
    still animates the glyphs of a `Text` individually rather than the `Text`.

    Passing an explicit `arg_creator` that wraps the submobject in a 1-tuple
    restores the manimgl behaviour: exactly one animation per direct submobject,
    whatever that submobject is made of.
    """
    return LaggedStartMap(animation_class, group, _one, **kwargs)
