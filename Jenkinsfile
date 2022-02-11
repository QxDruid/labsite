pipeline {
    agent any 
    
    stages {
        stage('Docker image build') {
            steps {
                sh "ls"
                sh "docker build -t labsite_${env.GIT_BRANCH} ."
                sh "docker images"
            }
        }

        stage('Deploy Staging') {
            when {
                expression {env.GIT_BRANCH == 'dev'}
            }

            steps {
                sh 'docker stop $(docker ps | grep labsite_dev | awk \'{print $1}\') || true'
                sh 'docker run -d --rm -p127.0.0.1:8090:8000 -v /home/web_host/webserver_dev/static/:/app/static/ -v /home/web_host/webserver_dev/database/:/database/ --env-file /home/web_host/webserver_dev/envfile.env  labsite_dev'
            }
        }

         stage('Deploy Production') {
            when {
                expression {env.GIT_BRANCH == 'master'}
            }

            steps {
                sh 'docker rm -f $(docker ps | grep labsite_master | awk \'{print $1}\') || true'
                sh 'docker run -d -p127.0.0.1:8000:8000 --rm -v /home/web_host/webserver/static/:/app/static/ -v /home/web_host/webserver/database/:/database/ --env-file /home/web_host/webserver/envfile.env labsite_master'
            }
        }
    }
}
