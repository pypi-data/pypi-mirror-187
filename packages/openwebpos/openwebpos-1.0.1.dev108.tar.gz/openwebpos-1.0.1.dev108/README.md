![Issues][issues-shield]
![MIT License][license-shield]
![PyPI - Wheel][wheel-shield]
![GitHub repo size](https://img.shields.io/github/repo-size/baezfb/OpenWebPOS?style=flat-square)

[![Python application](https://github.com/baezfb/OpenWebPOS/actions/workflows/python-app.yml/badge.svg)](https://github.com/baezfb/OpenWebPOS/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/baezfb/OpenWebPOS/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/baezfb/OpenWebPOS/actions/workflows/codeql-analysis.yml)
[![Dependency Review](https://github.com/baezfb/OpenWebPOS/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/baezfb/OpenWebPOS/actions/workflows/dependency-review.yml)

![GitHub contributors](https://img.shields.io/github/contributors/baezfb/OpenWebPOS?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/baezfb/OpenWebPOS)
![PyPI](https://img.shields.io/pypi/v/openwebpos)
![PyPI - Status](https://img.shields.io/pypi/status/openwebpos?style=flat-square)

# OpenWebPOS

OpenWebPOS is a web-based point of sale system written in python using the Flask framework.

## Built With

![Python](https://img.shields.io/badge/Python-3.8-blue)
[![Flask][flask-shield]][flask-url]
[![MaterializeCSS][MaterializeCSS-shield]][MaterializeCSS-URL]

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* Linux server with a non-root user with sudo privileges, and a firewall enabled
  * Updated the Server
    ```bash
    sudo apt update && sudo apt -y upgrade
    ```
  * Install python3-pip
    ```bash
    sudo apt install -y python3-pip
    ```
  * Install development tools
    ```bash
    sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
    ```
* Nginx installed and configured
    * Install Nginx
        ```bash
        sudo apt install -y nginx
        ```
    * Configure Firewall
        ```bash
        sudo ufw allow 'Nginx Full'
        ```
* A domain name pointing to the server's IP address

### Installation

* Create project directory and change to it
    ```bash
    mkdir ~/OpenWebPOS && cd ~/OpenWebPOS
    ```
* Create a virtual environment and activate it
    ```bash
    python3 -m venv venv && source venv/bin/activate
    ```
* Install
    - from PyPI (recommended)
        ```bash
        pip install openwebpos
        ```
    - from source
        ```bash
        git clone https://github.com/baezfj/OpenWebPOS.git
        pip install .
        ```

## Usage

* Create a wsgi.py or app.py file in the project directory

  ```python
  from openwebpos import open_web_pos
  from dotenv import load_dotenv
  
  load_dotenv('.env')
  
  application = open_web_pos()
  
  if __name__ == "__main__":
    application.run()
  ```

* Run the app

  ```bash
  $ python3 app.py
  ```

## Contributing

Contributions are what make the open source community such an amazing place to learned, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

[issues-shield]: https://img.shields.io/github/issues/baezfb/OpenWebPOS.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/baezfb/OpenWebPOS.svg?style=flat-square
[MaterializeCSS-URL]: https://materializecss.github.io/materialize/
[MaterializeCSS-shield]: https://img.shields.io/badge/MaterializeCSS-1.0.0-blue
[flask-shield]: https://img.shields.io/badge/Flask-2.2-blue
[flask-url]: https://flask.palletsprojects.com/en/2.2.x/
[wheel-shield]: https://img.shields.io/pypi/wheel/openwebpos?style=flat-square