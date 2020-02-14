#!groovy

def tryStep(String message, Closure block, Closure tearDown = null) {
    try {
        block()
    }
    catch (Throwable t) {
        slackSend message: "${env.JOB_NAME}: ${message} failure ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'

        throw t
    }
    finally {
        if (tearDown) {
            tearDown()
        }
    }
}


node {
    stage("Checkout") {
        checkout scm
    }

    stage('Test') {
        tryStep "test", {

            sh "docker-compose build && docker-compose up -d database && sleep 10 && docker-compose run -u root --rm app bash -c 'make flake test'"

        }, {
            sh "docker-compose down"
        }
    }

    stage("Build image") {
        tryStep "build", {
                docker.withRegistry("${DOCKER_REGISTRY_HOST}",'docker_registry_auth') {
                def image = docker.build("datapunt/overlastgebieden:${env.BUILD_NUMBER}")
                image.push()
            }
        }
    }
}


String BRANCH = "${env.BRANCH_NAME}"

if (BRANCH == "master") {

    node {
        stage('Push acceptance image') {
            tryStep "image tagging", {
                docker.withRegistry("${DOCKER_REGISTRY_HOST}",'docker_registry_auth') {
                    def image = docker.image("datapunt/overlastgebieden:${env.BUILD_NUMBER}")
                    image.pull()
                    image.push("acceptance")
                }
            }
        }
    }


    stage('Waiting for approval') {
        slackSend channel: '#ci-channel', color: 'warning', message: 'Overlastgebieden is waiting for Production Release - please confirm'
        input "Deploy to Production?"
    }

    node {
        stage('Push production image') {
            tryStep "image tagging", {
                docker.withRegistry("${DOCKER_REGISTRY_HOST}",'docker_registry_auth') {
                def image = docker.image("datapunt/overlastgebieden:${env.BUILD_NUMBER}")
                    image.pull()
                    image.push("production")
                    image.push("latest")
                }
            }
        }
    }

}