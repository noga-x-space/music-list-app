pipeline {
    agent {
        kubernetes {
            label 'dind-agent'
            yamlFile 'agent.yaml'
        }
    }
    environment {
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
        DOCKER_IMAGE = 'nogadocker/spotify:${BUILD_NUMBER}'
        DOCKER_CREDENTIALS_ID = credentials('dockerhub-credentials')
        // for when i use testing:
        // MONGO_USERNAME = credentials('mongo-username')
        // MONGO_PASSWORD = credentials('mongo-password')
        // MONGO_HOST = 'db'
        // MONGO_PORT = '27017'
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    git(
                        url: "https://oauth2:${GITHUB_TOKEN}@github.com/noga-x-space/music-list-app.git",
                        branch: 'app'
                    )
                }
            }
        }  // <-- Close the Checkout stage here

        stage('Hello World') {
            steps {
                echo 'Hello, World!'
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
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
