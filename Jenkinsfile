pipeline {
    agent any 
    
    stages {
        stage('Docker image build') {
            steps {
                sh "docker build -t labsite_${env.GIT_BRANCH} ."
            }
        }

        stage('Test') {
            steps {
                script {
                    RES = sh(script: "docker rm -f labsite_${env.GIT_BRANCH}_test || true" , returnStdout: true)
                    echo "${RES}"
                }

                sh "docker run -i --rm --name labsite_${env.GIT_BRANCH}_test -v /home/web_host/webserver_test/images/:/app/static/images/  labsite_${env.GIT_BRANCH} python3 tests.py"
                
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
                sh "docker run -d -p5000:8000 --rm --name labsite_dev -v /home/web_host/webserver_dev/images/:/app/static/images/ --env-file /home/web_host/webserver_dev/envfile labsite_dev"
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
                sh "docker run -d -p127.0.0.1:8000:8000 --rm --name labsite_master -v /home/web_host/webserver/images/:/app/static/images/ --env-file /home/web_host/webserver/envfile labsite_master"
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
