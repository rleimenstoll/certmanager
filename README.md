# Certificate Manager

## About
Certificate Manager is a project to discover and track the lifecycle changes of TLS certificates. At this time, users can create Endpoints, which represent a host and port combination for which to track. Certificates are discovered on polls against the endpoint and compared to existing values. If they are different, the endpoint is updated. A dashboard provides a glimpse at certificates that are expiring soon or expired.

## Architecture
This project consists of a Django WSGI application and a task queue that handles async events, such as scanning endpoints. Data is stored in a relational database. The task queue utilizes Celery and some message broker such as RabbitMQ or Amazon SQS.


### Running in a development instance
Docker and Docker Compose are prerequisites for developing on this project.

To develop on this application with a cloned repository, you can run (from the
base of the repo)
```
docker-compose up -d
```

This will spin up a container listening on port 8080 with an unpopulated but
prepared SQLite database. The application will launch and bind to localhost:8080.

### Running in production (AWS)
There are a number of primary components to an AWS deployment. Ideally, this would be managed with a SCM tool such as Terraform, CloudFormation, CloudForms, etc, although I haven't had the time to write a complete definition. High level requirements of the current production environment are listed below:

(See `doc/Certmanager.png` for arch diagram)

#### VPC
Networking is up to the end user's preference, however the production VPC is divided into a number of subnets across two availability zones. Application origin instances exist in subnets in private IP space with a NAT gateway to facilitate outbound communication, mainly with SQS. Load balancers and any bastion instances live in a dedicated subnet with an attached internet gateway.

Security groups are role based and limited as much as possible.

#### Database
The database is a fairly standard RDS MariaDB instance. A database with a user needs to be created for the application, although from there the app will create required tables as needed.

#### Web Origins and Task Queue
The application is packaged into Docker containers for portability. These containers are pushed into Amazon Elastic Container Registry, where they are then pulled into an ECS Fargate cluster. Services are defined for a webapp and taskqueue, both of which use the same container but different commands. Scaling options can be defined to utilize AWS's auto scale functionality. These services share a Execution Task Role (IAM Role) to gain access to various resources (such as SQS). The Amazon Docker logging driver is used to log to CloudWatch.

#### Load Balancer
Application requests are proxied through an application-type Amazon Load Balancer (ALB). The ECS cluster registers targets in the target group automatically. The load balancer lives in a dedicated subnet generally and is routed out through an internet gateway to satisfy public IP addressing requirements.

#### SQS
SQS is used to facilitate message communication between the taskqueue and web application.
