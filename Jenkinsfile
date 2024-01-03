pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    environment {
        // Docker
        LOCAL_IMG_TAG = "localhost/taskit:${BUILD_NUMBER}"
        TEST_NET = "taskit-nginx-net-${BUILD_NUMBER}"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building docker image ...'

                sh "docker build -t ${LOCAL_IMG_TAG} . --no-cache"
            }
        }

        stage('E2E') {
            stages {
                stage('Run') {
                    steps {
                        echo 'Running docker compose...'

                        sh """
                            export DOCKER_IMG=${LOCAL_IMG_TAG}
                            export NGINX_NET=${TEST_NET}
                            docker compose up -d
                        """
                    }
                }

                stage('Test') {
                    steps {
                        echo 'Running health check ...'
                        retry(20) {
                            sleep(time: 3, unit: 'SECONDS')
                            sh """
                                docker run --rm --network ${TEST_NET} \
                                    docker.io/curlimages/curl:latest \
                                    -fsSLI http://nginx:80/health --max-time 1
                            """
                        }
                    }
                }
            }

            post {
                always {
                    sh """
                        export DOCKER_IMG=${LOCAL_IMG_TAG}
                        export NGINX_NET=${TEST_NET}
                        docker compose down -v
                    """
                }
            }
        }

        stage('Publish') {
            when {
                anyOf {
                    branch 'main'
                    expression {
                        return BRANCH_NAME.startsWith('devops')
                    }
                }
            }

            stages {
                stage('Environment variable configuration') {
                    steps {
                        script {
                            // main
                            def remoteRegistry = '644435390668.dkr.ecr.eu-central-1.amazonaws.com/taskit'

                            // Devops
                            if (BRANCH_NAME =~ /^devops.*/) {
                                remoteRegistry = '644435390668.dkr.ecr.eu-central-1.amazonaws.com/taskit-test' 
                            }

                            // ECR
                            REMOTE_REGISTRY = "${remoteRegistry}"
                            REMOTE_IMG_TAG = "${REMOTE_REGISTRY}:${BUILD_NUMBER}"
                            REMOTE_IMG_LTS_TAG = "${REMOTE_REGISTRY}:latest"
                        }
                    }

                }

                stage('Tag') {
                    steps {
                        echo 'Tagging docker image ...'

                        sh """
                            docker tag ${LOCAL_IMG_TAG} ${REMOTE_IMG_TAG}
                            docker tag ${LOCAL_IMG_TAG} ${REMOTE_IMG_LTS_TAG}
                        """
                    }
                }

                stage('Push') {
                    steps {
                        echo 'Pushing image to registry'

                        sh """
                            aws ecr get-login-password --region eu-central-1 | \
                            docker login --username AWS --password-stdin ${REMOTE_REGISTRY}
                            docker push ${REMOTE_IMG_TAG}
                            docker push ${REMOTE_IMG_LTS_TAG}
                        """
                    }

                }

            }
            
            post {
                always {
                    sh """
                        docker rmi ${LOCAL_IMG_TAG}
                        docker rmi "${REMOTE_IMG_TAG}"
                        docker rmi "${REMOTE_IMG_LTS_TAG}"
                        docker logout ${REMOTE_REGISTRY}
                    """
                }
            }
        }

    }

    post {
        always {
            cleanWs()
        }
    }
}
