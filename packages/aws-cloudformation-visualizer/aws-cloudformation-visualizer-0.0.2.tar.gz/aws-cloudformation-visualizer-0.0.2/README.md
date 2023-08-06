# AWS CloudFormation Visualizer

## How to use

### Install AWS CloudFormation Visualizer

``` shell
pip install aws-cloudformation-visualizer
```

### Use in Code

``` python
import boot3
from cfn_visualizer import visualizer

client = boto3.client('cloudformation')

visualizer(client, stack_name='STACK NAME')
```