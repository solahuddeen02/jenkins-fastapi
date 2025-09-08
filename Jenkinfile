pipeline {
  agent none
  environment {
    // ชื่อ SonarQube server ที่ตั้งไว้ใน Jenkins > System
    SONARQ = 'SonarQube'
    IMAGE_NAME = 'fastapi-app:latest'
    CONTAINER_NAME = 'fastapi-app'
    APP_PORT = '8000'
  }

  stages {
    stage('Checkout') {
      agent any
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/solahuddeen02/jenkins-fastapi.git']]
        ])
      }
    }

    stage('Install & Test (Python)') {
      agent {
        docker { image 'python:3.11' }
      }
      steps {
        sh 'python --version'
        sh 'pip install --no-cache-dir -r requirements.txt'
        // สร้าง coverage.xml ให้ Sonar เห็น
        sh 'pytest --maxfail=1 -q --disable-warnings --cov=app --cov-report=xml'
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: '**/pytest*.xml'
          archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
        }
      }
    }

    stage('SonarQube Analysis') {
      agent {
        docker {
          image 'sonarsource/sonar-scanner-cli:latest'
          args "-v $WORKSPACE:/usr/src -w /usr/src"
        }
      }
      steps {
        withSonarQubeEnv("${SONARQ}") {
          sh '''
            sonar-scanner \
              -Dsonar.projectKey=fastapi-clean-demo \
              -Dsonar.sources=app \
              -Dsonar.tests=tests \
              -Dsonar.python.coverage.reportPaths=coverage.xml \
              -Dsonar.sourceEncoding=UTF-8
          '''
        }
      }
    }

    // (ถ้ามี Webhook + Quality Gate ตั้งใน SonarQube แล้ว ค่อยเปิดบล็อกนี้)
    // stage('Quality Gate') {
    //   agent any
    //   steps {
    //     timeout(time: 2, unit: 'MINUTES') {
    //       waitForQualityGate abortPipeline: true
    //     }
    //   }
    // }

    stage('Build Docker Image') {
      agent {
        docker {
          image 'docker:24.0-cli'
          args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
        sh 'docker build -t ${IMAGE_NAME} .'
      }
    }

    stage('Deploy Container') {
      agent {
        docker {
          image 'docker:24.0-cli'
          args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
        sh 'docker rm -f ${CONTAINER_NAME} || true'
        sh 'docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:8000 ${IMAGE_NAME}'
      }
    }
  }

  post {
    always {
      echo 'Pipeline finished'
    }
  }
}
