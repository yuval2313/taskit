pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
        skipDefaultCheckout(true)
    }

    environment {
        // Docker
        LOCAL_IMG_TAG = "localhost/taskit:${BUILD_NUMBER}"
        TEST_NET = "taskit-nginx-net-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Clean before build
                cleanWs(deleteDirs: true)
                // We need to explicitly checkout from SCM here
                checkout scm

                echo "Building ${env.JOB_NAME}..."
            }
        }

        stage('Environment variable configuration') {
            steps {
                script {
                    // main
                    def remoteRegistry = '644435390668.dkr.ecr.eu-central-1.amazonaws.com/taskit'

                    // devops
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

        stage('Build') {
            steps {
                echo 'Building docker image ...'

                sh "docker build -t ${LOCAL_IMG_TAG} ."
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

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    expression {
                        return BRANCH_NAME.startsWith('devops')
                    }
                }
            }

            environment {
                GITOPS_REPO_CRED_ID = 'taskit-gitops-github-cred'
                GITOPS_REPO_URL = 'git@github.com:yuval2313/taskit-gitops.git'
            }

            stages {
                stage('Checkout GitOps Repo') {
                    steps {
                        cleanWs(deleteDirs: true)

                        checkout scm: scmGit(
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[credentialsId: GITOPS_REPO_CRED_ID, url: GITOPS_REPO_URL]]
                        )
                    }
                }

                stage('Modify Image Tag') {
                    steps {
                        dir('taskit') {
                            sh 'cat values.yaml'

                            sh """
                                yq -yi \\'.taskit.image = \"${REMOTE_IMG_TAG}\" values.yaml\\'
                            """

                            sh 'cat values.yaml'
                        }
                    }
                }

                // stage('Push Changes') {
                //     steps {
                //         sh """
                //             git add .
                //             git commit -m 'Jenkins Deploy - Build #${BUILD_NUMBER}'
                //             git push origin main
                //         """
                //     }
                // }
            }

            post {
                always {
                    cleanWs(deleteDirs: true)
                }
            }
        }
    }

    post {
        always {
            cleanWs(deleteDirs: true)
            sh '''
                docker image prune -af
                docker volume prune -af
                docker container prune -f
                docker network prune -f
            '''
        }
    }
}
