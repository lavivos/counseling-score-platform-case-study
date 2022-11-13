"""Util functions"""

import streamlit as st
from joblib import load
from uuid import uuid4


def load_joblib(path):
    """load `joblib` object"""
    return load(path)


def get_metadata():
    """Returns features type metadata"""
    return {
        "binary": {
            "school", "sex", "address", "famsize", "Pstatus", "schoolsup",
            "famsup", "paid", "activities", "nursery", "higher", "internet",
            "romantic"
        },
        "numeric": {
            "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
            "famrel", "freetime", "goout", "Dalc", "Walc", "health",
            "absences", "FinalGrade"
        },
        "nominal": {"Mjob", "Fjob", "reason", "guardian"}
    }


def get_all_actionable_features():
    """List of potential actionable features and their metadata."""
    return {
        "studytime": {
            "type": "numeric",
            "min": 1,
            "max": 4,
            "default": 4
        },
        "absences": {
            "type": "numeric",
            "min": 0,
            "max": 20,
            "default": 0
        },
        "Dalc": {
            "type": "numeric",
            "min": 1,
            "max": 5,
            "default": 1
        },
        "Walc": {
            "type": "numeric",
            "min": 1,
            "max": 5,
            "default": 1
        },
        "freetime": {
            "type": "numeric",
            "min": 1,
            "max": 5,
            "default": 5
        },
        "schoolsup": {
            "type": "binary",
            "options": ("yes", "no"),
            "default": "yes"
        },
        "famsup": {
            "type": "binary",
            "options": ("yes", "no"),
            "default": "yes"
        },
        "paid": {
            "type": "binary",
            "options": ("yes", "no"),
            "default": "yes"
        }
    }


def adjust_page_ui_settings():
    """Setup page UI settings"""
    st.set_page_config(layout="wide",
                       page_title="Student Monitoring Platform",
                       page_icon="assets/favicon.png")
    st.markdown(
        '''<style>
            .css-1vq4p4l {padding-top: 2.5rem;}
         </style>
        ''',
        unsafe_allow_html=True,
    )


def add_title(title, color="black", size="1.5rem", background_color=None):
    """Add customed title"""
    style = f"text-align: center; color: {color}; font-size: {size}; "
    if background_color:
        style += f"background-color: {background_color}"
    return st.markdown(f"<h1 style='{style}'>{title}</h1>",
                       unsafe_allow_html=True)


def filter_and_export_component(estimator,
                                display_frame,
                                filter_features,
                                start_int_key: int,
                                ascending=True):
    """
    Constructs the view component for filtering and exporting the 
    students data given `filter_features`
    """
    holder_dict = dict()
    filtred_df = display_frame.copy()
    key = start_int_key
    for feature in filter_features:
        holder_dict[feature] = dict()
        holder_dict[feature]["min"] = int(estimator.X_target[feature].min())
        holder_dict[feature]["max"] = int(estimator.X_target[feature].max() +
                                          1)

        holder_dict[feature]["values"] = st.slider(
            f"Select range of {feature}:",
            holder_dict[feature]["min"],
            holder_dict[feature]["max"],
            (holder_dict[feature]["min"], holder_dict[feature]["max"]),
            key=key)
        filtred_df = filtred_df[
            (filtred_df[feature] >= holder_dict[feature]["values"][0])
            & (filtred_df[feature] <= holder_dict[feature]["values"][1])]
        key += 1

    filtred_df = filtred_df.sort_values(
        by=filter_features[0], ascending=ascending
    )  # Adding a sorting option would be better for later versions
    filename = "range_students_with_" + "_".join(([
        f"{feature}={value['values']}"
        for (feature, value) in holder_dict.items()
    ]))

    st.dataframe(filtred_df)
    st.download_button(label="Download range student data as CSV",
                       data=filtred_df.to_csv().encode('utf-8'),
                       file_name=f'{filename}.csv',
                       mime='text/csv',
                       key=key)
