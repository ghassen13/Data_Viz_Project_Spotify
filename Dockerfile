FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the entire project to the container
COPY . /app
COPY ./MyApp/Data /app/MyApp/Data


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Command to run both applications
CMD ["python", "/app/MyApp/eda_dashboard.py", "&", "sleep", "5", "&&", "python", "/app/MyApp/machine_learning.py"]
