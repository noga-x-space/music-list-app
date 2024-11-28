pipeline {
    agent {
        kubernetes {
            label 'dind-agent'
            yamlFile 'agent.yaml'
        }
    }
    environment {
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
        DOCKER_IMAGE = "nogadocker/spotify:${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = credentials('dockerhub-credentials')
        GITHUB_REPO = 'noga-x-space/music-list-app'
        // for when i use testing:
        // MONGO_USERNAME = credentials('mongo-username')
        // MONGO_PASSWORD = credentials('mongo-password')
        // MONGO_HOST = 'db'
        // MONGO_PORT = '27017'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                checkout scm
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
            when {
                    branch 'main'
                 }
            steps {
                 withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}
                        docker push ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('Update Helm values.yaml') {
            steps { 
                script {
                    // Use sed to replace the tag value in the values.yaml file
                    sh """
                        yq eval '.web.tag = \"${BUILD_NUMBER}\"' -i ./spotify-ish/values.yaml
                    """
                }
            }
        }
        stage('Commit and Push Changes to GitHub') {
            when {
                    branch 'main'
                 }
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    script {
                        sh """
                            git config --global user.email "jenkins@update.com"
                            git config --global user.name "jenkins"

                            
                            git branch
                        """

                        // Add and commit changes to values.yaml
                        sh """
                            git add ./spotify-ish/values.yaml
                            git status
                            git commit -m "Update web tag to ${BUILD_NUMBER}"
                            git remote -v
                            git push https://oauth2:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git main
                        """
                    }
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
