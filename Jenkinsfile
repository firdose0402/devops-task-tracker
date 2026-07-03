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
                bat 'docker build -t devops-task-tracker -f dockerfile .'
            }
        }

        stage('Test') {
            steps {
                echo 'Skipping tests'
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                docker stop task-tracker-container
                docker rm task-tracker-container
                docker run -d --name task-tracker-container -p 5000:5000 devops-task-tracker
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            bat 'docker images'
            bat 'docker ps -a'
        }
    }
}
