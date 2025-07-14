pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-calculator:latest'
        APP_CONTAINER_NAME = 'flask_calculator_app'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/vladyurik/app-Diplom.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh "docker rm -f ${APP_CONTAINER_NAME} || true"
                    sh "docker run -d --name ${APP_CONTAINER_NAME} -p 5000:5000 ${DOCKER_IMAGE}"
                }
            }
        }
    }
}
