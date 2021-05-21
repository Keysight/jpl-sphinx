// =====================================================================
// groovylint-disable BracesForMethod,BracesForTryCatchFinally,BracesForIfElse
// groovylint-disable MethodName,VariableName,ImplementationAsType
/* groovylint-disable-next-line CompileStatic, MethodParameterTypeRequired, MethodReturnTypeRequired, NoDef */
def call(body)
{
    Map config = [:]
    body.resolveStrategy = Closure.DELEGATE_FIRST
    body.delegate = config
    body()

    pipeline
    {
        agent any

        options
        {
            disableConcurrentBuilds()
            skipDefaultCheckout()
        }

        stages
        {
            stage('Checkout')
            {
                echo 'would checkout.'
            }

            stage('Get Host Info')
            {
                ShowHostInfo()
            }

            stage('Finalize')
            {
                echo 'I am done.'
            }
        }
    }
}
