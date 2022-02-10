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
                sh 'docker stop $(docker ps --filter ancestor=labsite_dev | tail -1 | awk \'{print $1}\') || true'
                sh 'docker run -d --rm -p8000:8000 -v /home/web_host/webserver_dev/static/:/app/static/ -v /home/web_host/webserver_dev/database/:/database/  labsite_dev'
            }
        }

         stage('Deploy Production') {
            when {
                expression {env.GIT_BRANCH == 'master'}
            }

            steps {
                sh 'docker rm -f $(docker ps --filter ancestor=labsite_master | tail -1 | awk \'{print $1}\') || true'
                sh 'docker run -d -p80:8000 --rm -v /home/web_host/webserver/static/:/app/static/ -v /home/web_host/webserver/database/:/database/ labsite_master'
            }
        }
    }
}
