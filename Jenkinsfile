pipeline {
    agent any
    environment {
        DOCKER_HUB_USERNAME = "harish0799"
        IMAGE_NAME = "mlops-demo"
        GIT_REPO = "https://github.com/harish9907/mlops-demo.git"
        IMAGE_TAG = "latest"
        KUBECONFIG_CRED = "kubeconfig" // Jenkins secret ID for kubeconfig file
    }
    stages {
        stage('Checkout Code') {
            steps {
                git "${GIT_REPO}"
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('DVC Pull Data') {
            steps {
                sh './venv/bin/dvc pull'
            }
        }

        stage('Train Model') {
            steps {
                sh './venv/bin/python src/train.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push Docker to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
                    sh "docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use kubeconfig stored as Jenkins secret
                withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBECONFIG_FILE')]) {
                    sh 'export KUBECONFIG=$KUBECONFIG_FILE'
                    // Update image in deployment
                    sh "kubectl set image deployment/mlops-demo mlops-demo=${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} --record"
                    // Apply service (only needed if first deployment or changed)
                    sh 'kubectl apply -f k8s/service.yaml'
                    // Optional: rollout status to wait for deployment
                    sh 'kubectl rollout status deployment/mlops-demo'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}

