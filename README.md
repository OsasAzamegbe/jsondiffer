<div id="top"></div>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
 -->


<!-- PROJECT LOGO -->
<br />
<div align="center">
<!--   <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h1 align="center">JSON DIFFER</h1>

  <p align="center">
    A diffing tool for JSON.
    <br />
    <a href="https://github.com/OsasAzamegbe/jsondiffer#readme"><strong>Explore the docs »</strong></a>
    <br />
    <br />
<!--     <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a> -->
<!--     · -->
    <a href="https://github.com/OsasAzamegbe/jsondiffer/issues">Report Bug</a>
    ·
    <a href="https://github.com/OsasAzamegbe/jsondiffer/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#building-and-running">Building and Running</a></li>
        <li><a href="#local-development">Local Development</a></li>
        <li><a href="#debian-package">Debian Package</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This tool written mainly in python for generating and printing diffs between two JSON files. The code has been designed in a way that makes it possible (in my opinion) to easily adapt the program as both a command line interface tool (a debian package for linux systems, is the main plan here) and in the near future (when time and energy permits), a web interface. I have (in my laziness) made use of some python 3.10 specific syntax, so this is the minimum compatible version of python you'll need for contributing to this project (unless you use docker for local development).

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With


* [Python](https://www.python.org/)
* [Docker](https://www.docker.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is a pretty simple project with just one requirement: 
* Docker (unless you do not enjoy the local development trope, in which case you'll be needing at least python 3.10).

### Prerequisites

You will need to have docker setup on your computer, which can be done fairly easily by following the steps on their [official documentation](https://docs.docker.com/get-docker/).


### Building and Running

1. install [python 3.10](https://www.python.org/downloads/) on your computer system and [get pip working](https://pip.pypa.io/en/stable/installation/).
2. navigate to your desired project directory
3. Clone the repo
   ```sh
   git clone https://github.com/OsasAzamegbe/jsondiffer.git
   ```
   (if you do not have git installed, take a brief detour and follow these [instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).
4. navigate to the project folder *__jsondiffer/__* 
   ```sh
   cd jsondiffer/
   ```
5. create a virtual environment.
   </br></br>
   Linux/MacOs
   ```sh
   pip install virtualenv && python3.10 -m venv venv && ./venv/bin/activate
   ```
   Windows:
   ```sh
   pip install virtualenv
   ```
   ```sh
   python3.10 -m venv venv 
   ```
   ```sh
   .\venv\Scripts\activate
   ```
   
6. install the required dev packages from the principal directory
   ```sh
   pip install -r requirements-dev.txt
   ```
7. once your virtual environment is up and running and you have your packages installed, you can run the tests with
   ```sh
   python -m pytest
   ```
8. You can now also run the program via the `main.py` file
   ```sh
   python jsondiffer/main.py --help
   ```

### Local Development
With docker fully setup on your system:

1. Follow **steps 2 - 4** from the <a href="#building-and-running">Building and Running</a> directions.
3. build the docker image
   ```sh
   docker-compose build
   ```
4. run the tests with
   ```sh
   docker-compose run --rm dev python3 -m pytest
   ```
5. you can also run a bash terminal (and hack away as you please) with
   ```sh
   docker-compose run --rm dev bash
   ```

### Debian Package

If you're not on a system with Debian support, you can follow the steps in <a href="#local-development">Local Development</a> to get a bash terminal from the Docker setup of this project before continuing below.

From your terminal window;
1. build your debian package with fpm
   ```sh
   fpm --python-bin python3 --python-package-name-prefix python3 -s python -t deb .
   ```
2. running ` ls ` should show a .deb file generated for this project
3. install the deb file generated from the previous step
   ```sh
   dpkg -i python3-jsondiffer_<versiontag>_all.deb
   ```
4. you now have the binary installed on your terminal and you can execute it with
   ```sh
   jsdiff --help
   ```

   Happy hacking! 😀

 </br></br>

<!-- USAGE EXAMPLES -->
## Usage

From an open terminal go through the steps detailed in <a href="#building-and-running">Building and Running</a>

1. navigate to the directory with the **main.py** file
2. run the jsondiffer program with
   ```sh
   python main.py <path/to/first/json/file> <path/to/second/json/file>
   ```
   for more help information, run
   ```sh
   python main.py [-h|--help]
   ```

If you have the debian package installed by following <a href="#debian-package">Debian Package</a>, you can use `jsdiff` to run the program, instead of `python main.py`
   ```sh
   jsdiff <path/to/first/json/file> <path/to/second/json/file>
   ```
   for more help information, run
   ```sh
   jsdiff [-h|--help]
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Check [CONTRIBUTING.md](https://github.com/OsasAzamegbe/jsondiffer/blob/main/CONTRIBUTING.md) for detailed instructions.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/OsasAzamegbe/jsondiffer/blob/main/LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

**Osamudiamen Azamegbe**
</br>[Medium](https://medium.com/@osas.azamegbe) 
</br>[osas.azamegbe@gmail.com](mailto:osas.azamegbe@gmail.com)

Project Link: [https://github.com/OsasAzamegbe/jsondiffer](https://github.com/OsasAzamegbe/jsondiffer)

<p align="right">(<a href="#top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/osamudiamen-azamegbe/
[product-screenshot]: images/screenshot.png

