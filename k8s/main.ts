import { Construct } from 'constructs';
import { App } from 'cdk8s';
import { DjangoApplication, PennLabsChart } from '@pennlabs/kittyhawk';

export class MyChart extends PennLabsChart {
  constructor(scope: Construct) {
    super(scope);

    const domain = 'penncfa.com';
    const image = 'pennlabs/common-funding-application';
    const secret = 'common-funding-application';

    new DjangoApplication(this, 'django', {
      deployment: {
        image,
        secret,
      },
      domains: [{ host: domain, paths: ['/']}],
      djangoSettingsModule: 'penncfa.settings.production',
    })
  }
}

const app = new App();
new MyChart(app);
app.synth();
