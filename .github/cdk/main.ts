import { Construct } from "constructs";
import { App, Stack, Workflow } from "cdkactions";
import { DeployJob, DjangoProject } from "@pennlabs/kraken";

export class CFAStack extends Stack {
  constructor(scope: Construct, name: string) {
    super(scope, name);
    const workflow = new Workflow(this, 'build-and-deploy', {
      name: 'Build and Deploy',
      on: 'push',
    });

    const cfaJob = new DjangoProject(workflow, {
      projectName: 'penncfa',
      imageName: 'common-funding-application',
      checkProps: {
        flake8: false,
        black: false,
      }
    });

    new DeployJob(workflow, {}, {
      needs: [cfaJob.publishJobId]
    });
  }
}

const app = new App();
new CFAStack(app, 'cfa');
app.synth();
