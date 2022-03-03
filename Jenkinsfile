pipeline {
    agent any 
    
    stages {
        stage('Docker image build') {
            steps {
                sh "docker build -t labsite_${env.GIT_BRANCH} ."
            }
        }

        stage('Deploy Staging') {
            when {
                expression {env.GIT_BRANCH == 'dev'}
            }

            steps {
                script {
                    RES = sh(script: "docker rm -f labsite_dev || true", returnStdout: true)
                    echo "${RES}"
                }
                sh "docker run -d -p5000:8000 --rm --name labsite_dev -v /home/web_host/webserver_dev/static/:/app/static/ --env-file /home/web_host/webserver_dev/envfile labsite_dev"
            }
        }

        stage('Deploy Production') {
            when {
                expression {env.GIT_BRANCH == 'master'}
            }

            steps {
                script {
                    RES = sh(script: "docker rm -f labsite_master || true", returnStdout: true)
                    echo "${RES}"
                }
                sh "docker run -d -p127.0.0.1:8000:8000 --rm --name labsite_master -v /home/web_host/webserver/static/:/app/static/ --env-file /home/web_host/webserver/envfile labsite_master"
            }
        }
        stage('Clean') {
            steps {
                script {
                    RES = sh(script: "docker rmi \$(docker images -f dangling=true -q) || true", returnStdout: true)
                    echo "${RES}"
                }
            }
        }
    }
}
