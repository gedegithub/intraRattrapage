pipeline {
    agent any
    environment {
        PYTHON_HOME = '/usr/bin/python3'
    }
    stages {
        stage('Build') {
            steps {
                script {
                    //  Installer les dépendances
                    sh 'python3 -m pip install -r requirements.txt' 
                    // Exécuter les script Python 
                    sh 'python3 scraper.py' 
                    // sh 'python3 html_generator.py'
                }
            }
        }
        stage('DetectChanges') {
            steps {
                script {
                    // Si jobs_previous.csv existe, comparer avec jobs.csv
                    def changed = true
                    if (fileExists('data/jobs_previous.csv')) {
                        // Compare les fichiers via md5sum pour plus de performance mais moins de sécurité
                        def oldHash = sh(script: "md5sum data/jobs_previous.csv | cut -d' ' -f1", returnStdout: true).trim()
                        def newHash = sh(script: "md5sum data/jobs.csv | cut -d' ' -f1", returnStdout: true).trim()
                        if (oldHash == newHash) {
                            echo "Aucune nouvelle offre"
                            // Journaliser
                            sh 'echo "Aucune nouvelle offre" >> logs/log.txt'
                            currentBuild.result = 'SUCCESS'
                            return
                        }
                    }
                    // Copier jobs.csv → jobs_previous.csv
                    sh 'cp data/jobs.csv data/jobs_previous.csv'
                }
            }
        }
        stage('Conversion') {
            steps {
                sh 'python3 html_generator.py'
            }
        }
        stage('Validation') {
            steps {
                sh 'pytest -v test_validation.py'
            }
        }
        stage('Deploy') {
            steps {
                // Requires Jenkins to run as a user with permission to write to /usr/share/nginx/html/
                sh 'cp public/index.html /usr/share/nginx/html/index.html'
            }
        }
    }
    post {
        always {
            // Archiver le fichier data.csv comme artefact dans Jenkins
            archiveArtifacts artifacts: 'data/jobs.csv,public/index.html,logs/log.txt', fingerprint: true
        }
    }
}
