#Grant super-user privileges
Start-Process Powershell -Verb runAs


#create a directory
New-Item -ItemType directory -Path C:\DEVOPS-Copy\DevOps-Course-Starter

#Check which Python versions are available 
#If python is not installed, get the version and store in directory location above

$ispythoninstalled = python --version
if ($ispythoninstalled) { python --version } else { Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe" -OutFile "C:\DEVOPS-Copy\DevOps-Course-Starter/python-3.7.0.exe" }


#command to install Python
C:\DEVOPS-Copy\DevOps-Course-Starter/python-3.7.0.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

##update the path 
ENV:PATH="$ENV:PATH;C:\Users\Rajesh\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts"

#Check if poetry is already installed 
 

#Check if poetry is already installed . If not, install it
poetry --version
$ispoetryinstalled = poetry --version
if ($ispoetryinstalled) {poetry --version} else { (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python }

#To get started you need Poetry''s bin directory (%USERPROFILE%\.poetry\bin) in your `PATH`

$env:PATH += ";%USERPROFILE%\.poetry\bin;"

#Install application dependencies
cd C:\DEVOPS-Copy\DevOps-Course-Starter # change dir
#git init
git clone https://github.com/CorndelWithSoftwire/DevOps-Course-Starter.git

#Create a virtual environment
poetry install

cp .env.template .env

#Launch the application
poetry run flask run

