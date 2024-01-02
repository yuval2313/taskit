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
        // TODO: Registry config
        // REGISTRY =
        // REGISTRY_REPO =

        // TODO: remote image tags
        // REMOTE_IMG_TAG = "${REGISTRY}/${REGISTRY_REPO}/taskit:${BUILD_NUMBER}"
        // REMOTE_IMG_LTS_TAG = "${REGISTRY}/${REGISTRY_REPO}/taskit:latest"

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

        stage('Run') {
            steps {
                echo 'Running docker compose...'

                sh """
                    export DOCKER_IMG=${LOCAL_IMG_TAG}
                    export NGINX_NET=${TEST_NET}
                """

                sh 'docker compose up'
            }
        }

        stage('Test') {
            steps {
                echo 'Running health check ...'
                retry(20) {
                    sleep(time: 3, unit: 'SECONDS')
                    sh """
                        docker run --rm --network "${TEST_NET}" \
                            docker.io/curlimages/curl:latest \
                            -fsSLI http://nginx:80/health --max-time 1
                    """
                }
            }
        }

        // stage('Tag') {
        //     steps {
        //         echo 'Tagging docker image ...'

        //         sh 'docker tag "${LOCAL_IMG_TAG}" "${REMOTE_IMG_TAG}"'

        //         sh 'docker tag "${LOCAL_IMG_TAG}" "${REMOTE_IMG_LTS_TAG}"'
        //     }
        // }

        // stage('Push') {
        //     steps {
        //         sh '''
        //             docker login "${REGISTRY}" -u "${REGISTRY_CRED_USR}" -p "${REGISTRY_CRED_PSW}"
        //         '''

    //         sh '''
    //             docker push "${REMOTE_IMG_TAG}"
    //             docker push "${REMOTE_IMG_LTS_TAG}"
    //             docker logout "${REGISTRY}"
    //         '''
    //     }
    // }
    }

    post {
        always {
            sh """
                docker compose down -v
                docker rmi ${LOCAL_IMG_TAG}
            """
            // docker rmi "${REMOTE_IMG_TAG}"
            // docker rmi "${REMOTE_IMG_LTS_TAG}"
            // docker logout "${REGISTRY}"
            cleanWs()
        }
    }
}
