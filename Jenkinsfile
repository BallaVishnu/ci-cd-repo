pipeline {
  agent any

  environment {
    // Docker image name — change if your DockerHub username is different
    IMAGE = "ballavishnu/ci-cd-repo:jenkins"
    VENV  = ".venv"
    PY    = "python"   // change to full path if needed, e.g. C:\\Python39\\python.exe
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
        powershell """
          ${env.PY} -m venv ${env.VENV}
          .\\${env.VENV}\\Scripts\\python -m pip install --upgrade pip
          .\\${env.VENV}\\Scripts\\pip install -r requirements.txt
        """
      }
    }

    stage('Run Tests') {
      steps {
        powershell ".\\${env.VENV}\\Scripts\\pytest -q"
      }
    }

    stage('Build Docker Image') {
      steps {
        powershell "docker build -t ${env.IMAGE} ."
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                          usernameVariable: 'DOCKER_USER',
                                          passwordVariable: 'DOCKER_PASS')]) {
          powershell """
            echo $env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin
            docker push ${env.IMAGE}
          """
        }
      }
    }

    stage('Deploy Container (host)') {
      steps {
        powershell """
          docker pull ${env.IMAGE}
          docker stop ci-cd-demo || Write-Output 'no container to stop'
          docker rm ci-cd-demo || Write-Output 'no container to remove'
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
