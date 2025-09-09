pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'my-fastapi-image:latest'
        DOCKER_CLI_IMAGE = 'docker:24.0-cli'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/solahuddeen02/fastapi-demo.git' // เปลี่ยนเป็น repo ของคุณ
            }
        }

        stage('Pull Docker CLI') {
            steps {
                script {
                    // ดึง Docker CLI image มาก่อนใช้
                    sh "docker pull ${DOCKER_CLI_IMAGE}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // ใช้ docker container รัน Docker CLI
                withDockerContainer(image: "${DOCKER_CLI_IMAGE}", args: "-v /var/run/docker.sock:/var/run/docker.sock -u root") {
                    // ตรวจสอบว่า Dockerfile อยู่ใน root ของ workspace
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // login ก่อน push ถ้าจำเป็น
                    // sh "docker login -u USERNAME -p PASSWORD your-registry.com"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
        }
    }
}
