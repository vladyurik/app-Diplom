pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-calculator:latest'
        APP_CONTAINER_NAME = 'flask_calculator_app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vladyurik/app-Diplom.git'
            }
        }

        stage('Lint') {
            steps {
                script {
                    docker.image('python:3.10').inside('-u root') {
                        sh 'pip install flake8'
                        sh 'flake8 .'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Run Container for Testing') {
            steps {
                script {
                    sh "docker rm -f ${APP_CONTAINER_NAME} || true"
                    sh "docker run -d --name ${APP_CONTAINER_NAME} -p 5000:5000 ${DOCKER_IMAGE}"
                    sh "sleep 3" // немного подождать, чтобы приложение запустилось
                }
            }
        }

        stage('Run Integration Tests') {
            steps {
                script {
                    docker.image('python:3.10').inside('-u root') {
                        sh 'pip install pytest requests'
                        sh 'pytest tests/'
                    }
                }
            }
        }

        stage('Restart for Deployment') {
            steps {
                script {
                    sh "docker stop ${APP_CONTAINER_NAME}"
                    sh "docker rm -f ${APP_CONTAINER_NAME}"
                    sh "docker run -d --name ${APP_CONTAINER_NAME} -p 5000:5000 ${DOCKER_IMAGE}"
                }
            }
        }
    }
}
