from setuptools import setup, find_packages

setup(
    name="soluzion_server",
    version="0.2.5",
    description="This is a restructured implementation of a Flask + SocketIO server for use with Soluzion framework "
    "problems, with an emphasis on supporting custom clients.",
    author="James Gale",
    author_email="jpgale@cs.washington.edu",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",  # Specify the minimum version of Python required
    install_requires=[
        "setuptools>=53.0.0",
        "flask~=3.0.3",
        "flask-socketio~=5.3.6",
        "python-socketio[client]~=5.11.2",
        "prompt_toolkit~=3.0.43",
        "flask-cors~=4.0.1",
    ],
    entry_points={
        "console_scripts": [
            "soluzion_server=soluzion_server.main:main",
            "soluzion_client=soluzion_test_client.test_client:main",
        ]
    },
)
