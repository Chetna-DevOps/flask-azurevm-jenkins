# Flask Restaurant Review App — Azure VM Deployment with Jenkins

A Flask + PostgreSQL web app deployed to an Azure Virtual Machine using a Jenkins CI/CD 
pipeline with a remote Ubuntu agent.

## Base application

This project starts from Microsoft's official sample app 
([Azure-Samples/msdocs-flask-postgresql-sample-app](https://github.com/Azure-Samples/msdocs-flask-postgresql-sample-app)). 
The application code (Flask routes, models, templates) is from this sample. Everything 
related to deployment — VM configuration, Nginx + Gunicorn setup, Jenkins pipeline and 
agent configuration was built independently.

## What this project demonstrates

- Provisioning and configuring an Azure Virtual Machine (Ubuntu)
- Setting up Gunicorn as a systemd service for production-grade Flask serving
- Configuring Nginx as a reverse proxy in front of Gunicorn
- Building a multi-stage Jenkins pipeline for automated CI/CD
- Configuring Azure VM as a Jenkins agent (controller-agent architecture)
- Automating pipeline triggers using GitHub Webhooks + ngrok

## Architecture

```
GitHub (push to main)
→ GitHub Webhook triggers Jenkins (via ngrok)
→ Jenkins Controller (local machine)
→ Jenkins Agent (Azure Ubuntu VM)
→ git pull latest code
→ pip install dependencies
→ flask db upgrade (PostgreSQL migrations)
→ sudo systemctl restart flaskapp
→ Nginx (reverse proxy, port 80)
→ Gunicorn (WSGI server, port 8000)
→ Flask App
→ Azure Database for PostgreSQL

```
## Tech Stack
| Category | Technology |
|---|---|
| App Framework | Flask + Python |
| Database | Azure Database for PostgreSQL |
| Web Server | Nginx (reverse proxy) |
| WSGI Server | Gunicorn (systemd service) |
| CI/CD | Jenkins |
| Cloud | Azure Virtual Machine (Ubuntu 20.04) |
| Webhook | GitHub Webhooks + ngrok |

## Jenkins Pipeline Stages

Stage 1: Pull Code → git pull latest code from GitHub onto VM
Stage 2: Install Deps → pip install -r requirements.txt in virtualenv
Stage 3: Run Migrations → flask db upgrade to apply DB schema changes
Stage 4: Restart App → systemctl restart flaskapp (zero-config reload)

## Jenkins Controller-Agent Architecture
Rather than running pipeline steps on the local Windows machine (Jenkins Controller),
the Azure Ubuntu VM is configured as a Jenkins Agent. This means:
- All pipeline steps execute directly on the VM
- No SSH commands needed inside the pipeline
- Clean separation between Controller (orchestration) and Agent (execution)

## Key Technical Decisions & Why
**Gunicorn over Flask dev server** — Flask's built-in server is single-threaded and 
not suitable for production. Gunicorn runs multiple worker processes and handles 
concurrent requests properly.

**Nginx as reverse proxy** — Nginx efficiently handles incoming HTTP traffic, serves 
static files, and forwards dynamic requests to Gunicorn. Industry standard setup.

**systemd service for Gunicorn** — Ensures the app automatically restarts on VM 
reboot or crashes, without any manual intervention.

**Azure VM as Jenkins Agent** — Running Jenkins agent on the same Ubuntu VM where 
the app lives avoids Windows/Linux compatibility issues and simplifies the pipeline.

## Challenges Faced & How They Were Resolved
| Challenge | Root Cause | Fix Applied |
|---|---|---|
| App not accessible on browser | Port 80 blocked by Azure NSG | Added HTTP inbound rule in Network Security Group |
| Nginx couldn't reach Gunicorn | Gunicorn bound to TCP port, Nginx looking for Unix socket | Changed proxy_pass to http://127.0.0.1:8000 |
| SSH Agent plugin failed on Windows | Plugin designed for Linux, not Windows | Moved Jenkins agent to Azure Ubuntu VM |
| `git.exe` not found on Ubuntu | Jenkins configured on Windows, passed .exe to Linux agent | Installed git on VM, changed path in Jenkins Tools config |
| `source` command not found | Jenkins uses `dash` shell by default, not `bash` | Added `#!/bin/bash` shebang to sh blocks in Jenkinsfile |

## Application Screenshots
### Home Page
![Home Page](screenshots/home-page.png)
### Jenkins Pipeline Success
![Jenkins Pipeline](screenshots/jenkins-pipeline-success.png)
### Jenkins Stages View
![Jenkins Stages](screenshots/jenkins-stages-view.png)
### GitHub Webhook Configuration
![Webhook](screenshots/github-webhook.png)
### Azure VM Overview
![Azure VM](screenshots/azure-vm-overview.png)
### Nginx Configuration
![Nginx](screenshots/nginx-config.png)
### Gunicorn Systemd Service
![Gunicorn Service](screenshots/gunicorn-service-status.png)


PostgreSQL, Redis, GitHub Actions, Azure App Service
