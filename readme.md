## About the dashboard application:

You can easily test the deployed application in the following link: [Counseling Dashboard](https://lavivos-counseling-platform-view-tbmadm.streamlit.app).

Otherwise you can:

- Run the application in your local machine after installing the required dependencies, using the command **streamlit run view.py**.
- Build the image using the provided `Dockerfile` and run the application in a docker container:
  - `docker build -t counseling_platform .`
  - `docker run counseling_platform`

The provided `Dockerfile`, can also be used to easily deploy the application to other server providers (Certainly some configuration could be needed depending on the server provider)

**Finally, please note that the provided notebook is not part of the main project, but is provided to show the approach details. Reading the notebook is mandatory to understand the modelling process and generally the thought process behind the application.**
