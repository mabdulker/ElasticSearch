# Use an official Python runtime as the base image
FROM continuumio/miniconda3:4.10.3 

# Set the working directory in the container
WORKDIR /code

# COPY ./app /code/app
# COPY ./environment.yml /code/environment.yml

# Install any needed packages specified in environment.yml
RUN conda env update -n base --file /code/environment.yml

# # Make port 8000 available to the world outside this container
# EXPOSE 8000rn", "app.main:app", "--host", "0.0.0.0", "--reload"]
