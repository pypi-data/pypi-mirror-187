FROM railflow/blazetest:PYTHON_VERSION

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/

# Install Chrome dependencies
RUN python3 -m pip install --upgrade pip -q && \
    python3 -m pip install -r /tmp/requirements.txt -q

# Copy project files and tests
ADD . ${LAMBDA_TASK_ROOT}/
ADD .blazetest/tests_runner_handler ${LAMBDA_TASK_ROOT}/tests_runner_handler

CMD ["tests_runner_handler.handler.run_tests"]