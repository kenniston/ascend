# Controller: Characterization of attacks and network anomalies for autonomous vehicles

The Controller project aims to develop methodologies and techniques 
for advanced discovery of cyber attacks in essential contexts for a 
digital society: transport infrastructure and access network.

<br/>

## Develop Tools

The Controller project was developed in **Python**. To install the required tools, 
run the following command:

```shell
sudo apt-get install python-pip python-dev build-essential
```

Using **pip**, install virtual environment tool:

```shell
pip install virtualenv
```

## Develop Environment

First, create a new folder and clone this repository into the created folder:

```shell
mkdir controller && cd controller
```

```shell
git clone https://github.com/c2dc/controller-papers framework
```

<br/>

## Python Virtual Environment

To preserve the local python enviroment it is highly recommended to create 
a Python Virtual Environment. To create the virtual use the following 
command:

```shell
python3 -m venv venv
```

In the framework directory, activate the created virtual environment:

```shell
source ./venv/bin/activate
```

Install Jupyter Kernel in the created virtual environment:

```shell
pip install ipykernel
```

## How to build

```shell
pip install –-user –-upgrade setuptools wheel
```

*Important: if you are installing the project in a virtual environment, 
remove '--user' and '--upgrade' parameter from the above command.*

<br/>

```shell
python3 setup.py sdist
```

## Install the package on local machine or Virtual Environment

To install the **controller** framework on local machine or Virtual 
Environment, run the following command from root directory:

```shell
pip install .
```

***To install the development version use the following command:***
```shell
pip install -e .
```

 ## How to develop

 To create a new feature extends the ***controller.base.Feature*** 
 class and implement the ***process*** method. 