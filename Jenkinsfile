def findLatestTag(tags, releaseVersion) {
    def tagArray = tags.split('\n')
    def latestTag = null

    // Iterate through the tags to find a tag starting with releaseVersion
    for (tag in tagArray) {
        if (tag.startsWith(releaseVersion)) {
            latestTag = tag
            break
        }
    }

    return latestTag // returns latestTag variable
}

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
        REPO_CRED_ID = 'taskit-github-cred'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Version calculation') {
            steps {
                script {
                    sshagent(credentials: ["${REPO_CRED_ID}"]) {
                        def releaseVersion = sh(script: 'cat version.txt', returnStdout: true).trim()

                        // Get all tags
                        sh 'git fetch --tags'
                        def tags = sh(script: 'git tag -l --merge | sort -r -V', returnStdout: true).trim()

                        def latestTag = findLatestTag(tags, releaseVersion)
                        def calculatedVersion = ''

                        if (latestTag) {
                            /* groovylint-disable-next-line UnusedVariable */
                            def (major, minor, patch) = latestTag.tokenize('.')
                            patch = patch.toInteger() + 1
                            calculatedVersion = "${releaseVersion}.${patch}"
                        } else {
                            calculatedVersion = "${releaseVersion}.1"
                        }

                        env.LATEST_TAG = latestTag
                        env.RELEASE_VERSION = releaseVersion
                        env.CALCULATED_VERSION = calculatedVersion
                    }
                }
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

                    // Remote
                    REMOTE_REGISTRY = "${remoteRegistry}"
                    REMOTE_IMG_TAG = "${REMOTE_REGISTRY}:${CALCULATED_VERSION}"
                    REMOTE_IMG_LTS_TAG = "${REMOTE_REGISTRY}:latest"

                    // Local
                    LOCAL_IMG_TAG = "localhost/taskit:${CALCULATED_VERSION}"
                    TEST_NET = "taskit-nginx-net-${CALCULATED_VERSION}"
                }
            }
        }

        stage('Debug') {
            steps {
                echo '---------------DEBUG----------------------'

                echo "LATEST_TAG: ${LATEST_TAG}"
                echo "RELEASE_VERSION: ${RELEASE_VERSION}"
                echo "CALCULATED_VERSION: ${CALCULATED_VERSION}"
                echo "REMOTE_REGISTRY: ${REMOTE_REGISTRY}"
                echo "REMOTE_IMG_TAG: ${REMOTE_IMG_TAG}"
                echo "REMOTE_IMG_LTS_TAG: ${REMOTE_IMG_LTS_TAG}"
                echo "LOCAL_IMG_TAG: ${LOCAL_IMG_TAG}"
                echo "TEST_NET: ${TEST_NET}"

                echo '---------------DEBUG----------------------'
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
                stage('Tag Image') {
                    steps {
                        echo 'Tagging docker image ...'

                        sh """
                            docker tag ${LOCAL_IMG_TAG} ${REMOTE_IMG_TAG}
                            docker tag ${LOCAL_IMG_TAG} ${REMOTE_IMG_LTS_TAG}
                        """
                    }
                }

                stage('Push Image') {
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

                stage('Git Tag & Clean') {
                    steps {
                        sshagent(credentials: ["${REPO_CRED_ID}"]) {
                            sh """
                                git clean -f
                                git reset --hard
                                git tag ${CALCULATED_VERSION}
                                git push origin ${CALCULATED_VERSION}
                            """
                        }
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
                        cleanWs()

                        checkout scm: scmGit(
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[credentialsId: GITOPS_REPO_CRED_ID, url: GITOPS_REPO_URL]]
                        )
                    }
                }

                stage('Modify Image Tag') {
                    steps {
                        dir('taskit') {
                            sh """
                                yq -yi \'.taskit.image = \"${REMOTE_IMG_TAG}\"\' values.yaml
                            """
                        }
                    }
                }

                stage('Push Changes') {
                    when {
                        branch 'main'
                    }

                    environment {
                        GIT_USER_NAME = 'Jenkins'
                        GIT_USER_EMAIL = 'lyuval1210@gmail.com'
                    }

                    steps {
                        sshagent(credentials: ["${GITOPS_REPO_CRED_ID}"]) {
                            sh """
                                git config user.name '${GIT_USER_NAME}'
                                git config user.email '${GIT_USER_EMAIL}'

                                git add .
                                git commit -m 'Jenkins Deploy - Build #${BUILD_NUMBER}, Version ${CALCULATED_VERSION}'

                                git remote add origin ${GITOPS_REPO_URL}
                                git push -u origin main
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
