pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-task-tracker -f dockerfile .'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest tests/'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop task-tracker-container || true
                docker rm task-tracker-container || true

                docker run -d \
                  --name task-tracker-container \
                  -p 5000:5000 \
                  devops-task-tracker
                '''
            }
        }
    }
}
