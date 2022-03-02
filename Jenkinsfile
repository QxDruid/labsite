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
                    RES = sh(script: "docker rm -f \$(docker ps | grep labsite_dev | cut -f 1 -d ' ') || true", returnStdout: true)
                    echo "${RES}"
                }
                sh "docker run -d -p5000:8000 --rm -v /home/web_host/webserver_dev/static/:/app/static/ --env-file /home/web_host/webserver_dev/envfile labsite_dev"
            }
        }

        stage('Deploy Production') {
            when {
                expression {env.GIT_BRANCH == 'master'}
            }

            steps {
                script {
                    RES = sh(script: "docker rm -f \$(docker ps | grep labsite_master | cut -f 1 -d ' ') || true", returnStdout: true)
                    echo "${RES}"
                }
                sh "docker run -d -p127.0.0.1:8000:8000 --rm -v /home/web_host/webserver/static/:/app/static/ --env-file /home/web_host/webserver/envfile labsite_master"
            }
        }
        stage('Clean') {
            steps {
                sh "docker rmi \$(docker images -f “dangling=true” -q)"
            }
        }
    }
}
