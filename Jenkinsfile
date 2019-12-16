pipeline {
	agent { 
		docker { image 'python:2.7.17' }
	}
	environment {
		SLACK_API_TOKEN	= credentials('SLACK_API_TOKEN')
		SLACK_CHANNEL_NAME	= credentials('SLACK_CHANNEL_NAME')
		SLACK_TIMBOT_USER_ID = credentials('SLACK_TIMBOT_USER_ID')
	}
	stages {
		stage('Install Requirements') {
			steps {
				sh 'pip install -r requirements.txt'
			}
		}
		stage('PEP8 Check') {
			steps {
				sh 'flake8'
			}
		}
	}
	post {
		always {
			archiveArtifacts artifacts: 'build/libs/**/*.jar', fingerprint: true
			junit 'build/reports/**/*.xml'
		}
        success {
            echo 'I think this would qualify as not smart, but genius....and a very stable genius at that!'
        }
        unstable {
            echo 'Jenkins is so self righteous and ANGRY! Loosen up and have some fun. Timbot is doing well!'
        }
        failure {
            echo '.....THIS SHOULD NEVER HAPPEN TO A TIMBOT AGAIN!'
        }		
	}
}
