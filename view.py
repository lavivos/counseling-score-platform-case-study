"""View main page"""

import streamlit as st
import pandas as pd
from services import *

# ignore chained_assignment warning
pd.options.mode.chained_assignment = None
adjust_page_ui_settings()

# Setup sidebar
with st.sidebar:
    add_title("Student Monitoring Application",
              background_color="#cccccc",
              size="1.8rem")
    with st.container():
        # setup visualisation type
        st.header("1) Chart settings:")
        st.markdown("""<h4>Select visualisation type:</h4>""",
                    unsafe_allow_html=True)
        option = st.sidebar.selectbox('Select visualisation type',
                                      ('static', 'interactive'),
                                      index=1,
                                      label_visibility="collapsed")
        width = st.sidebar.slider("Figure width", 1, 25, 12)
        height = st.sidebar.slider("Figure height", 1, 25, 6)
        plot_params = {"width": width, "height": height}
    with st.container():
        st.header("2) Advisor strategy settings:")
        # setup actionable features
        actionable_features = get_all_actionable_features()

        for feature, conf in actionable_features.items():
            if conf["type"] == "numeric":
                actionable_features[feature]["value"] = st.sidebar.slider(
                    feature,
                    min_value=conf["min"],
                    max_value=conf["max"],
                    value=conf["default"])
            else:
                actionable_features[feature][
                    "value"] = st.sidebar.select_slider(
                        feature,
                        options=conf["options"],
                        value=conf["default"])

# load student data
df_data = pd.read_csv("data/student_data.csv", index_col="StudentID")
X, y = df_data.drop(["FinalGrade", "FirstName", "FamilyName"],
                    axis=1), df_data["FinalGrade"]

# Setup and run default improvement strategy
strategy_config = {
    feature: data["value"]
    for feature, data in actionable_features.items()
}
estimator = DefaultImprovementStrategy(X, y, strategy_config=strategy_config)
estimator.apply_improvement_strategy()
# reintegrate student features
estimator.X_target[["FirstName", "FamilyName", "FinalGrade"
                    ]] = df_data[["FirstName", "FamilyName", "FinalGrade"]]
# dataframe used for data export
display_frame = estimator.X_target[[
    "FirstName", "FamilyName", "PerformanceGain", "Complexity", "FinalGrade",
    "ExpectedGrade"
]].reset_index().copy()

st.markdown("""
    # About the dashboard:

    To evaluate the **value** of students counseling, the main retained measure is the one labeled as `PerformanceGain`. 
    A student's performance gain is the difference between his expected grade given a counseling strategy (`ExpectedGrade`) 
    and his actual final grade (`FinalGrade`). Thus, making `PerformanceGain` a practical measure of the interest of 
    counseling a student (the practical **value** being at its highest for students with higher `PerformanceGain`). Other measures like 
    `ExpectedGrade` and `FinalGrade` are suggested below.

    For the **complexity** of counseling the retained heuristic measure labeled `Complexity` represents the total range of 
    modifications for each student given a counseling strategy. For example, using our default retained counseling strategy 
    settings (see the section `Advisor strategy settings` in the side bar), for a student with (studytime=1, absences=12, Dalc=3, Walc=4, 
    freetime=1, schoolsup=1, famsup=no) the **complexity** would be `(4-1)[for studytime]+(12-0)[for absences]+(3-1)[for Dalc]+(4-1)[for Walc]+
    (5-1)[for freetime]+(1-1)[for schoolsup]+(1-0)[for famsup] = 25`. This measure is representative of the difficulty of helping students
    and thus of the **complexity** of counseling.

    - **Note:** *The expected grades are estimated using our artificial intelligence model for grading students given their demographic, social and school related features.*
""")

# Dashboard body section
st.markdown("""# Students prioritization dashboard:""")
tab1, tab2, tab3 = st.tabs([
    "Complexity vs Performance gain", "Complexity  vs Expected grades",
    "Complexity vs Actual grades"
])

st_displayer = st.pyplot if option == "static" else st.plotly_chart
with tab1:
    st_displayer(
        scatter_plot(estimator.X_target["PerformanceGain"],
                     estimator.X_target["Complexity"],
                     option,
                     xlabel="Performance gain",
                     color="orange",
                     **plot_params))
    st_displayer(priority_scatter_plot(estimator, y, option, **plot_params))

    st.header("Filter/Export students of interest:")
    filter_and_export_component(
        estimator,
        display_frame,
        filter_features=["PerformanceGain", "Complexity"],
        ascending=False,
        start_int_key=1)

with tab2:
    st_displayer(
        scatter_plot(estimator.X_target["ExpectedGrade"],
                     estimator.X_target["Complexity"],
                     option,
                     color="green",
                     alpha=0.7,
                     **plot_params))
    st.header("Filter/Export students of interest:")
    filter_and_export_component(
        estimator,
        display_frame,
        filter_features=["Complexity", "ExpectedGrade"],
        ascending=True,
        start_int_key=4)
with tab3:
    st_displayer(
        scatter_plot(y,
                     estimator.X_target["Complexity"],
                     option,
                     color="red",
                     alpha=0.7,
                     **plot_params))
    st.header("Filter/Export students of interest:")
    filter_and_export_component(estimator,
                                display_frame,
                                filter_features=["Complexity", "FinalGrade"],
                                ascending=True,
                                start_int_key=7)

# Download the target data created from the ongoing strategy
with st.sidebar:
    st.header("3) Export strategy performance measures:")
    st.download_button(
        label="Download output measures data as CSV",
        data=estimator.X_target[[
            "FirstName", "FamilyName", "Complexity", "FinalGrade",
            "ExpectedGrade", "PerformanceGain"
        ]].to_csv().encode('utf-8'),
        file_name='strategy_output_data.csv',
        mime='text/csv',
    )
