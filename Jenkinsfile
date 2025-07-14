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
                    // подождать, пока контейнер стартует
                    sleep(time: 5, unit: 'SECONDS')
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    sh """
                        docker exec ${APP_CONTAINER_NAME} sh -c 'apk add --no-cache curl || apt-get update && apt-get install -y curl'
                        docker exec ${APP_CONTAINER_NAME} sh -c '
                            STATUS_CODE=\$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
                            echo "Status code: \$STATUS_CODE"
                            [ "\$STATUS_CODE" -ne 200 ] && exit 1 || exit 0
                        '
                    """
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                   sh """
                       docker exec ${APP_CONTAINER_NAME} sh -c 'apk add --no-cache curl || apt-get update && apt-get install -y curl'
                       docker exec ${APP_CONTAINER_NAME} sh -c '
                           curl -s http://localhost:5000/ > /response.html
                       '
                       docker cp ${APP_CONTAINER_NAME}:/response.html response.html
                   """
                   archiveArtifacts artifacts: 'response.html', fingerprint: true
                }
            }
    }
        
    }
}
