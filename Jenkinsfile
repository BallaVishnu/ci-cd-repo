pipeline {
    agent any

    environment {
        IMAGE = "ballavishnu/ci-cd-repo:jenkins"
        VENV = "venv"
        PY = "python3"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                  branches: [[name: '*/main']],
                  userRemoteConfigs: [[
                    url: 'https://github.com/BallaVishnu/ci-cd-repo.git',
                    credentialsId: 'github-creds'
                  ]]
                ])
            }
        }

        stage('Create venv & install') {
            steps {
                sh """
                    ${env.PY} -m venv ${env.VENV}
                    . ${env.VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    . ${env.VENV}/bin/activate
                    pytest -q
                """
            }
        }

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
        always { 
            echo "Build finished: ${currentBuild.currentResult}"
        }
        success { 
            echo "Pushed image: ${env.IMAGE}"
        }
        failure { 
            echo "Build failed - check console output"
        }
    }
}
