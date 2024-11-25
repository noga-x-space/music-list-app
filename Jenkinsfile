pipeline {
    agent {
        kubernetes {
            label 'dind-agent'
            yamlFile 'agent.yaml'
        }
    }
    environment {
        DOCKER_IMAGE = 'nogadocker/spotify:latest'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials' // Replace with your Jenkins Docker credentials ID
    }

    stages {
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
    }


        
}
