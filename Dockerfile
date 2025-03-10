FROM python:3.9-bullseye

# 1. Update apt and install tools needed:
#    - apt-transport-https, gnupg2, curl  => so we can add Microsoft apt repo
#    - unixodbc-dev                       => ODBC core libraries (needed by pyodbc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    gnupg2 \
    curl \
    unixodbc-dev

# Add Microsoft package repo & install msodbcsql17 + unixodbc-dev
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
 
RUN apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev \
 && rm -rf /var/lib/apt/lists/*

 # Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY app/ /app/app/
COPY ddl* /app/
COPY run.py /app/

# Create a directory for DDL files with correct permissions
RUN mkdir -p /app/ddl && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# 6. Expose port 8000
EXPOSE 8000

# 7. Jalankan aplikasi
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Command to run the application
CMD ["python", "run.py"]



# FROM python:3.9-bullseye AS builder

# # Setup build environment
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     apt-transport-https \
#     gnupg2 \
#     curl \
#     unixodbc-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Add Microsoft package repo & install msodbcsql18
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update \
#     && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Set work directory for the build stage
# WORKDIR /build

# # Install dependencies
# COPY requirements.txt .
# RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# # Start a new stage for the final image
# FROM python:3.9-slim-bullseye

# # Install runtime dependencies and tini
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     apt-transport-https \
#     gnupg2 \
#     curl \
#     unixodbc-dev \
#     tini \
#     && rm -rf /var/lib/apt/lists/*

# # Add Microsoft package repo & install msodbcsql18 for runtime
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update \
#     && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
#     && rm -rf /var/lib/apt/lists/*

# # Create non-root user
# RUN groupadd -r appuser && useradd -r -g appuser appuser

# # Set working directory
# WORKDIR /app

# # Copy wheels from builder stage
# COPY --from=builder /build/wheels /wheels

# # Install dependencies
# RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
#     && rm -rf /wheels

# # Copy application code
# COPY app/ /app/app/
# COPY run.py /app/

# # Create a directory for DDL files with correct permissions
# RUN mkdir -p /app/ddl && chown -R appuser:appuser /app

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PYTHONIOENCODING=UTF-8

# # Switch to non-root user
# USER appuser

# # Expose port for the application
# EXPOSE 8000

# # Health check to ensure application is responding
# HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

# # Use tini as entrypoint for proper signal handling
# ENTRYPOINT ["/usr/bin/tini", "--"]

# # Command to run the application
# CMD ["python", "run.py"]
