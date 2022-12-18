import os
from setuptools import setup, find_packages

install_requires = [
    ('flake8', '5.0.4'),
    ('pydantic', '1.10.2'),
    ('psycopg2-binary', '2.9.5'),
    ('Flask', '2.1.0'),
    ('Flask-WTF', '1.0.1'),
    ('sqlalchemy', '1.4.44'),
    ('prometheus-client', '0.15.0'),
    ('python-dotenv', '0.21.0'),
]

CI_PROJECT_NAME = os.environ.get("CI_PROJECT_NAME", "data-proccessing-worker")
ARTIFACT_VERSION = os.environ.get("ARTIFACT_VERSION", "local")
CI_PROJECT_TITLE = os.environ.get("CI_PROJECT_TITLE", "Воркер актуализации скоринга")
CI_PROJECT_URL = os.environ.get("CI_PROJECT_URL", "https://gitlab.in.axept.com/rshb/data-proccessing-worker")


setup(
    name=CI_PROJECT_NAME,
    version=ARTIFACT_VERSION,
    description=CI_PROJECT_TITLE,
    url=CI_PROJECT_URL,
    install_requires=[">=".join(req) for req in install_requires],
    python_requires=">=3.9.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            CI_PROJECT_NAME + " = " + "data_proccessing_worker.main:execute",
        ]
    }
)
