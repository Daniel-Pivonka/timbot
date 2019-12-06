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
		stage('build') {
			steps {
				sh '''
					pip install -r requirements.txt
					python timbot.py
				'''
			}
		}
	}
	post {
		always {
			archiveArtifacts artifacts: 'build/libs/**/*.jar', fingerprint: true
			junit 'build/reports/**/*.xml'
		}
	}
}
