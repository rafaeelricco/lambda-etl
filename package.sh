#!/bin/bash
echo "This shell script is used to create a package the project."
/usr/bin/python3.8 -m venv env # Create a virtual environment
. env/bin/activate # Activate the virtual environment 

cp -r lambda_function.py env/lib/python3.8/site-packages/ # Copy the lambda function to the site-packages directory

cd env/lib/python3.8/site-packages/ # Go to the site-packages directory

# Zip all files in the site-packages directory
zip -r package.zip *

cd - # Go back to the project directory
cp env/lib/python3.8/site-packages/package.zip . # Copy the zip file to the project directory

deactivate # Deactivate the virtual environment
rm -rf tmp_venv # Remove the virtual environment