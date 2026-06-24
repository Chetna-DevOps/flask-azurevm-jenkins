pipeline {
    // Run on our Azure VM agent instead of local Windows machine
    agent { label 'azure-vm' }

    stages {
        stage('Pull Code') {
            steps {
                sh 'cd /app && git pull origin main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    cd /app
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Migrations') {
            steps {
                sh '''
                    cd /app
                    source venv/bin/activate
                    flask db upgrade
                '''
            }
        }

        stage('Restart App') {
            steps {
                sh 'sudo systemctl restart flaskapp'
            }
        }
    }

    post {
        success {
            echo 'Flask app deployed successfully!'
        }
        failure {
            echo 'Deployment failed. Check logs above.'
        }
    }
}
