pipeline {
    agent any

    environment {
        IMAGE_NAME = "mlops-demo"
        DOCKER_HUB = "harish0799/mlops-demo"
        DOCKER_CREDENTIALS = "dockerhub-creds"   // Jenkins DockerHub credentials ID
        PYTHON = "python3"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-username/mlops-demo.git'
            }
        }

        stage('Setup Python & Install Deps') {
            steps {
                sh '''
                ${PYTHON} -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install dvc[all]
                '''
            }
        }

        stage('Reproduce Pipeline with DVC') {
            steps {
                sh '''
                . venv/bin/activate
                dvc pull
                dvc repro
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest -f docker/Dockerfile .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}", usernameVariable: "DOCKER_USER", passwordVariable: "DOCKER_PASS")]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker tag $IMAGE_NAME:latest $DOCKER_HUB:latest
                    docker push $DOCKER_HUB:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }
}

