FROM python:3.9.0
RUN pip install pipenv

# Create app directory
ENV APP_HOME /app/web
WORKDIR $APP_HOME
ENV PYTHONPATH=$PYTHONPATH:$APP_HOME

# Copying this separately prevents re-running pip install on every code change.
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --ignore-pipfile
ENV PATH=/root/.local/share/virtualenvs/web-ijJmU-Nl/bin:$PATH

# Copy utility files
COPY .env .
COPY alembic.ini .

# Copy over bash file
COPY startup.sh .
RUN chmod +x ./startup.sh

# Copy the rest of the files over
COPY . .
CMD ["bash", "/app/web/startup.sh"]
