"""Streamlit helpers that work across old and new versions."""

import inspect

import streamlit as st


def image_wide(image, **kwargs):
    kwargs.pop("use_container_width", None)
    kwargs.pop("use_column_width", None)
    params = inspect.signature(st.image).parameters
    if "use_container_width" in params:
        st.image(image, use_container_width=True, **kwargs)
    elif "use_column_width" in params:
        st.image(image, use_column_width=True, **kwargs)
    else:
        st.image(image, **kwargs)


def button_wide(label: str, *, disabled: bool = False, key=None) -> bool:
    params = inspect.signature(st.button).parameters
    kw: dict = {"disabled": disabled}
    if key is not None:
        kw["key"] = key
    if "use_container_width" in params:
        kw["use_container_width"] = True
    return st.button(label, **kw)
