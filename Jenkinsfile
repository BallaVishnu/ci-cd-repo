pipeline {
    agent any

    environment {
        IMAGE = "vishnu933/ci-cd-repo:jenkins"
    }

    stages {


        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${env.IMAGE} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    sh """
                        echo "$PASS" | docker login -u "$USER" --password-stdin
                        docker push ${env.IMAGE}
                    """
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh """
                    docker pull ${env.IMAGE}
                    docker stop ci-cd-demo || true
                    docker rm ci-cd-demo || true
                    docker run -d -p 5000:5000 --name ci-cd-demo ${env.IMAGE}
                """
            }
        }
    }

    post {
        success { echo "Build and push completed!" }
        failure { echo "Pipeline failed. Check logs." }
    }
}
