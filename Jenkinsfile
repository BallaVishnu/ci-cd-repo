pipeline {
  agent any

  environment {
    // replace YOUR_DOCKERHUB_USERNAME with your docker hub username
    IMAGE_NAME = "vishnu933/todo-app"
    IMAGE_TAG  = "${env.GIT_COMMIT?.take(7) ?: 'latest'}"
    FULL_IMAGE = "${env.IMAGE_NAME}:${env.IMAGE_TAG}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        // Use PowerShell on Windows agents (change to 'sh' if on Linux)
        powershell label: 'pip install requirements', script: '''
          python -m pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run tests') {
      steps {
        powershell label: 'run pytest', script: '''
          pytest -q
        '''
      }
    }

    stage('Build Docker image') {
      when {
        expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
      }
      steps {
        script {
          // this uses the Docker Pipeline plugin
          dockerImage = docker.build(env.FULL_IMAGE)
        }
      }
    }

    stage('Push to Docker Hub') {
      when {
        expression { dockerImage != null }
      }
      steps {
        script {
          // uses credentials id 'dockerhub-creds' that you added in Jenkins
          docker.withRegistry('', 'dockerhub-creds') {
            dockerImage.push()
            // optionally also push 'latest' tag
            dockerImage.push('latest')
          }
        }
      }
    }
  } // stages

  post {
    always {
      echo "Build finished with status: ${currentBuild.currentResult}"
    }
    success {
      echo "Image pushed: ${env.FULL_IMAGE}"
    }
    failure {
      echo "Build failed - check console output"
    }
  }
}
