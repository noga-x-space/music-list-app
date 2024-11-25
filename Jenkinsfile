pipeline {
    agent {
        kubernetes {
            label 'dind-agent'
            yamlFile 'agent.yaml'
        }
    }
    environment {
        DOCKER_IMAGE = 'nogadocker/spotify:${BUILD_NUMBER}'
        DOCKER_CREDENTIALS_ID = credentials('dockerhub-credentials')
        MONGO_USERNAME = credentials('mongo-username')
        MONGO_PASSWORD = credentials('mongo-password')
        MONGO_HOST = 'db'
        MONGO_PORT = '27017'
    }

    stages {
        // for test stage run python -m pytest app/test_app.py -v
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Hello World') {
            steps {
                script {
                    echo 'Hello, World!'
                }
            }
        }

        stage('Add Docker-compose'){
            steps{
                script{
                    sh '''
                        apk add --no-cache docker-compose
                        docker-compose build
                    '''
                }
            }
        }
        stage('Build and Test') {
            steps {
                sh '''
                    docker-compose build
                    echo "Docker Compose build completed successfully"
                '''
            }
        }

        stage('Build Production Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE} .
                    echo "Production Docker image built successfully"
                '''
            }
        }

        // stage('Push Docker Image') {
        //     steps {
        //         sh '''
        //             echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
        //             docker push ${DOCKER_IMAGE}
        //             docker logout
        //         '''
        //     }
        // }
        stage('Push Docker Image') {
            steps {
                withDockerRegistry(credentialsId: 'dockerhub-credentials') {
                    sh '''
                        docker push ${DOCKER_IMAGE}
                    '''
                }
            }
        }

    }
    
    post {
        always {
            node {
                sh '''
                    docker-compose down -v || true
                    docker logout || true
                '''
            }
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}