FROM python:3.13-slim

# Create non-root user
ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y git bash-completion curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=2.2.1
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry
ENV POETRY_VIRTUALENVS_CREATE=false

# Setup bash completion
RUN echo '# Enable bash completion' >> /home/$USERNAME/.bashrc && \
    echo 'if [ -f /etc/bash_completion ]; then' >> /home/$USERNAME/.bashrc && \
    echo '    . /etc/bash_completion' >> /home/$USERNAME/.bashrc && \
    echo 'fi' >> /home/$USERNAME/.bashrc && \
    echo '' >> /home/$USERNAME/.bashrc && \
    echo '# Python environment' >> /home/$USERNAME/.bashrc && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/$USERNAME/.bashrc && \
    echo '' >> /home/$USERNAME/.bashrc && \
    echo '# Poetry completion' >> /home/$USERNAME/.bashrc && \
    echo 'poetry completions bash >> ~/.bash_completion 2>/dev/null || true' >> /home/$USERNAME/.bashrc && \
    chown $USERNAME:$USERNAME /home/$USERNAME/.bashrc

WORKDIR /workspace

USER $USERNAME
