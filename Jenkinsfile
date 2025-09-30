pipeline {
    agent any

    environment {
        DOCKER_HUB = 'harish0799/mlops-demo'
        IMAGE_NAME = 'mlops-demo'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python & Install Deps') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate && pip install --upgrade pip
                . venv/bin/activate && pip install -r requirements.txt
                '''
            }
        }

        stage('DVC Pull Data') {
            steps {
                sh '. venv/bin/activate && dvc pull'
            }
        }

        stage('Reproduce Pipeline with DVC') {
            steps {
                sh '. venv/bin/activate && dvc repro'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_HUB:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                 usernameVariable: 'DOCKER_USER',
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $DOCKER_HUB:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    '''
                }
            }
        }
    }
}

