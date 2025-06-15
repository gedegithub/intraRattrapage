pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        PYTHON_HOME = '/usr/bin/python3'
    }
    stages {
        stage('Prepare') {
            steps {
                // Créer l'environnement virtuel
                sh 'python3 -m venv $VENV_DIR'
            }
        }
        stage('Install') {
            steps {
                script {
                    // Activer environment venv
                    sh '''
                        . $VENV_DIR/bin/activate
                        python3 -m pip install --upgrade pip
                    '''
                    // Installer les dépendances
                    sh 'python3 -m pip install -r requirements.txt'
                    // Exécuter les scripts Python (décommenter si besoin)
                    // sh 'python3 scraper.py'
                    // sh 'python3 html_generator.py'
                }
            }
        }
        stage('Run') {
            steps {
                // Exécuter le script Python et gérer les erreurs
                script {
                    try {
                        sh '''
                            . $VENV_DIR/bin/activate
                            python3 scraper.py
                        '''
                    } catch (err) {
                        echo "Erreur lors de l'exécution de scraper.py : ${err}"
                        currentBuild.result = 'FAILURE'
                        throw err
                    }
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
                // nano /etc/sudoers && add jenkins ALL=(ALL) NOPASSWD: /bin/cp
                sh 'sudo cp public/index.html /usr/share/nginx/html/index.html'
            }
        }
    }
    post {
        always {
            // Archiver le fichier data.csv comme artefact dans Jenkins
            archiveArtifacts artifacts: 'data/jobs.csv,public/index.html,logs/log.txt', fingerprint: true

            // Nettoyage de l’environnement virtuel
            sh 'rm -rf $VENV_DIR || true'
        }
        failure {
            // Actions à effectuer en cas d'échec du pipeline
            echo 'Le pipeline a échoué. Consultez les logs.'
        }
    }
}
