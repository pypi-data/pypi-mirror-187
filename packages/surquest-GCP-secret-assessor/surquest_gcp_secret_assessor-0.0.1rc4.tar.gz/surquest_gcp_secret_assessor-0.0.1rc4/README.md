# Introduction

This project is designed to simplify access to the secrets stored in the Secret Manager within Google Cloud Platform (GCP) during the application development life cycle. 

Let's imagine you are developing an application running in Cloud Run using a git repository for code versioning and CI/CD pipelines orchestration. In this case the secrets can be mounted to the Cloud Run container as environmental variables. This provided easy and fast access to the secrets within the deployed application but during the development lifecycle it may cause complications. To keep the secrets only in Secret Manager and avoid a situation of having the secrets on multiple places as environment variables and/or Git repository variables you can use this project.

# Quick Start

``python
from surquest.GCP.secret_assessor import Secret

secret_value = Secret.get("my-secret-name")
``