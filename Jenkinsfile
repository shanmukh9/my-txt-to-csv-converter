pipeline {
    agent any

    environment {
        REPO_URL = 'https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-text-to-csv-converter'
        DOCKER_IMAGE = 'shanmukh9/my-python-app:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${REPO_URL}", credentialsId: 'codecommit-credentials'
            }
        }

        stage('Run Streamlit App') {
            steps {
                script {
                    sh '''
                        # Pull the Docker image from Docker Hub
                        docker pull ${DOCKER_IMAGE}

                        # Run the Docker container
                        docker run --rm -p 8501:8501 ${DOCKER_IMAGE}
                    '''
                }
            }
        }
    }
}
