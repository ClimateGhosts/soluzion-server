from setuptools import setup, find_packages

setup(
    name="soluzion_server",  # Replace with the name of your package
    version="0.1.0",  # Replace with your package's version
    description="Your package description",  # Optional: add a brief description
    author="James Gale",
    author_email="jpgale@cs.washington.edu",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",  # Specify the minimum version of Python required
    install_requires=["setuptools>=53.0.0", "flask~=3.0.3", "flask-socketio~=5.3.6"],
    entry_points={
        "console_scripts": [
            "soluzion_server=soluzion_server.main:main",
            "soluzion_client=soluzion_test_client.test_client:main",
        ]
    },
)
