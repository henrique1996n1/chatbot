# chatbot
## Overview
Small and medium-sized businesses (SMBs) often face challenges when it comes to leveraging the sophisticated tools and resources that larger companies have at their disposal. Limited resources and manpower can hinder SMBs from effectively engaging with customers and optimizing their operations. Our project aims to bridge this gap by providing SMBs with a powerful toolset accessible through one of the most ubiquitous communication platforms: messaging.

## Project Objectives
The primary objectives of this project are as follows:

Create a Basic Chatbot: We have developed a simple yet effective chatbot tailored for SMBs. This chatbot allows businesses to engage with their customers through messaging, offering a streamlined way to provide services and interact with their audience.

Promotional Message Sending: Our tooling includes a feature that enables SMBs to send promotional messages, such as coupons, to their customers. This helps businesses reach their target audience more effectively.

Statistical Insights: The project also incorporates a statistics collection mechanism. SMBs can track and analyze customer engagement with their promotional messages, including click-through rates and other relevant metrics.

## Running the application
You have two ways to run the application. The first one is using docker containers and the another is running locally in your machine.

### Using docker container
To run using docker it's just run the commands `make create-docker-image` and  `make container-run`
1. To build a Docker image, execute `make create-docker-image`.
2. Launch a Docker container with `make container-run`.

### Local
1. Create and Activate Virtual Environment
- Run make `create-virtual-env` to create a virtual environment.
- Activate the virtual environment by running `source virtualenv/bin/activate`.
2. Install Dependencies
- Generate the requirements file by running `make update-requirements`.
- Install the required dependencies using `make requirements-install`.
3. Database Setup
- Create the database schema by running `make create-database`.
- Populate the database with initial data using `make insert-data`.
4. Run the Application
- Start the application by executing `make run`.

## Testing
In our testing strategy, we utilize edge cases to comprehensively cover all potential code paths. To execute the entire suite of tests, simply run the command `make test`.