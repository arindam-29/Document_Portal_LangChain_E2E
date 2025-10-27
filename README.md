# Project Setup Guide

## Create Project Folder and Environment Setup

```bash
# Create a new project folder
mkdir <project_folder_name>

# Move into the project folder
cd <project_folder_name>

# Open the folder in VS Code
code .

# Create a new Conda environment with Python 3.10
conda create -p <env_name> python=3.10 -y

# Activate the environment (use full path to the environment)
conda activate <path_of_the_env>

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Initialize Git
git init

# Stage all files
git add .

# Commit changes
git commit -m "<write your commit message>"

# Push to remote (after adding remote origin)
git push

# Cloning the repository
git clone https://github.com/arindam-29/Agentic_Document_Portal_LangChain_E2E.git

# Create new branch
git checkout -b "<branch_name>"

# Switch barch 
git switch main 

```
## Minimum Requirements for the Project

### LLM Models
- **Groq** (Free)
- **OpenAI** (Paid)
- **Gemini** (15 Days Free Access)
- **Claude** (Paid)
- **Hugging Face** (Free)
- **Ollama** (Local Setup)

### Embedding Models
- **OpenAI**
- **Hugging Face**
- **Gemini**

### Vector Databases
- **In-Memory**
- **On-Disk**
- **Cloud-Based**

## API Keys

### GROQ API Key
- [Get your API Key](https://console.groq.com/keys)  
- [Groq Documentation](https://console.groq.com/docs/overview)

### Gemini API Key
- [Get your API Key](https://aistudio.google.com/apikey)  
- [Gemini Documentation](https://ai.google.dev/gemini-api/docs/models)


## Running the App on AWS ECS 
- **AWS Account** 
- **AWS IAM User**
    * Get your IAM User: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    * Add them in Github secrets
- **AWS Secret Manager add your API Keys**
- **Create and setup AWS ECR**
- **Create AWS ECS Cluster**
    * Create ECS Service
- **Pull the latest code from github**
- **Update the files in .github/workflows folder with AWS details**
- **Add the AWS IAM roles for the user, use 'incline_policy.json' file to create two incline policies**
- **Go to AWS EC2 and Security Group and update inbound details**
    * Click on Security Group and update inbound details: Type->Custom TCP, Port range->8080, Source->Anywhere IPV4 0.0.0.0/0
- **Go to ECS Custer -> Service -> Task -> Public_IP**
    * Open in any browser (https://Public_IP:8080)
- **Go to AWS CloudWatch -> Log groups -> use running task id to view the log** 


