@Library('caelum@refs/tags/v0.8.0') _

pipeline{
    agent{
        docker{
            image '169.254.149.20:6001/arch_python_git_ghost_opencv_baw:v1.37.3'
        }
    }
    stages{
        stage('integrate'){
            steps{script{baw.integrate()}}
        }
        stage('setup'){
            steps{script{baw.setup()}}
        }
        stage('test'){
            failFast true
            parallel{
                stage('doc'){
                    steps{
                        script{baw.doctest()}
                    }
                }
                stage('fast'){
                    steps{
                        script{baw.fast()}
                    }
                }
                stage('long'){
                    steps{
                        script{baw.longrun()}
                    }
                }
            }
        }
        stage('pre-release'){
            when{not{branch 'master'}}
            steps{sh 'baw publish --pre'}
        }
        stage('quality'){
            failFast true
            parallel{
                stage('lint'){
                    steps{
                        script{baw.lint()}
                    }
                }
                stage('format'){
                    steps{
                        script{baw.format()}
                    }
                }
            }
        }
        stage('generate'){
            steps{
                sh 'baw --docken generate all'
            }
        }
        stage('all'){
            steps{
                sh 'baw --docken test all -n32'
            }
        }
        //stage('all'){
        //    steps{
        //        script{baw.all(docken=true)}
        //    }
        //}
        stage('release'){
            steps{
                script{
                    publish.release()
                    baw.rebase()
                }
            }
        }
    }
}
