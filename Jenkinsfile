pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-calculator:latest'
        APP_CONTAINER_NAME = 'flask_calculator_app'
        TEST_CONTAINER_NAME = 'flask_calculator_test'
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

        stage('Unit Tests') {
            steps {
                script {
                    docker.image('python:3.10').inside('-u root') {
                        sh 'pip install pytest'
                        sh 'pytest tests/unit'
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
                    // Запуск временного тестового контейнера
                    sh "docker run -d --rm --name ${TEST_CONTAINER_NAME} -p 5001:5000 ${DOCKER_IMAGE}"
                    sleep time: 5, unit: 'SECONDS' // Подождать пока поднимется
                }
            }
        }

        stage('Integration Tests') {
            steps {
                script {
                    docker.image('python:3.10').inside('-u root') {
                        sh 'pip install requests'
                        sh 'pytest tests/integration'
                    }
                }
            }
        }

        stage('Cleanup Test Container') {
            steps {
                script {
                    sh "docker stop ${TEST_CONTAINER_NAME} || true"
                }
            }
        }

        stage('Restart for Deployment') {
            steps {
                script {
                    sh "docker stop ${APP_CONTAINER_NAME} || true"
                    sh "docker rm -f ${APP_CONTAINER_NAME} || true"
                    sh "docker run -d --name ${APP_CONTAINER_NAME} -p 5000:5000 ${DOCKER_IMAGE}"
                }
            }
        }
    }
}
