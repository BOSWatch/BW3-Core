timestamps {
    timeout(10) {
        node() {

            stage('Prepare & Checkout') {
                checkout([$class: 'GitSCM', branches: [
                    [name: '**']
                ], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [
                    [credentialsId: '', url: 'https://github.com/BOSWatch/BW3-Core.git']
                ]])
                sh '''
                mkdir _results/ || true
                '''

            }
            stage('pyLint') {
                sh '''
                # pylint and coverage
                pylint --disable=W1401,C0103 --max-line-length=150 --output-format=parseable --exit-zero \$(find ./ -name "*.py") > _results/pylint.log
                '''
            }
            stage('pyTest & cov') {
                sh '''
                # test and coverage
                pytest --junitxml=_results/pytest.xml --cov=boswatch/ test/ --cov-report=xml:_results/pytest-cov.xml
                '''
            }
            stage('Doxygen & Cloc') {
                sh '''
                # doxygen
                doxygen "_gen/doxygen.ini" > _results/doxygen.log
                '''

                sh '''
                # cloc
                cloc --by-file --xml --out=_results/cloc.xml boswatch/ test/ plugins/ config/
                '''
            }
            stage('Publish results') {
                warnings canComputeNew: false, canResolveRelativePaths: false, categoriesPattern: '', defaultEncoding: '', excludePattern: '', failedTotalHigh: '20', failedTotalLow: '400', failedTotalNormal: '200', healthy: '100', includePattern: '', messagesPattern: '', parserConfigurations: [
                    [parserName: 'PyLint', pattern: '_results/pylint.log']
                ], unHealthy: '400', unstableTotalHigh: '10', unstableTotalLow: '200', unstableTotalNormal: '100'
                junit healthScaleFactor: 5.0, testDataPublishers: [
                    [$class: 'StabilityTestDataPublisher']
                ], testResults: '_results/pytest.xml'
                sloccountPublish encoding: '', pattern: '_results/cloc.xml'
                cobertura autoUpdateHealth: false, autoUpdateStability: false, classCoverageTargets: '95, 60, 50', coberturaReportFile: '_results/pytest-cov.xml', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '95, 60, 50', maxNumberOfBuilds: 0, methodCoverageTargets: '95, 60, 50', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
                openTasks canComputeNew: false, defaultEncoding: '', excludePattern: '', failedTotalHigh: '5', failedTotalLow: '50', failedTotalNormal: '20', healthy: '5', high: 'FIXME, BUG', ignoreCase: true, low: 'NOTE', normal: 'TODO', pattern: '**/*.py', unHealthy: '50', unstableTotalHigh: '2', unstableTotalLow: '25', unstableTotalNormal: '10'
                archiveArtifacts allowEmptyArchive: false, artifacts: '_results/*.*,config/*.*', caseSensitive: true, defaultExcludes: true, fingerprint: false, onlyIfSuccessful: false
            }
        }
    }
}
