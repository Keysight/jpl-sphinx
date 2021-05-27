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
                steps
                {
                    echo 'would checkout.'
                }
            }

            stage('Get Host Info')
            {
                steps
                {
                    ShowHostInfo()
                }
            }

            stage('Finalize')
            {
                steps
                {
                    echo 'I am done.'
                }
            }
        }
    }
}
