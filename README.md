Evaluation of the Wildcatter ID using variable elimination:

```python

from idpy.models.examples import wildcatter
from idpy.inference.variable_elimination import *

idiag = wildcatter()
print(idiag)

removal_order = ["O", "D", "S", "T"]
inf = VariableElimination(idiag, removal_order)

inf.run()


print("\n====== Results ====== ")
print(f"MEU = {inf.meu}")

for d in idiag.decisions:
    print(f"optimal policy for {d}:")
    pol_d = inf.optimal_policy[d]
    print(pol_d)
    print(pol_d.values)
    
    eu_d = inf.expected_util[d]
    print(eu_d)
    print(eu_d.values)
    print("----")


```


Output: 
```
<IDiagram [T, D], [C, P], [S, O], [u(T), u(D,O), p(S|T,O), p(O)]>

====== Results ====== 
MEU = 22.5
optimal policy for T:
<Potential util(), cardinality = ()>
0
<Potential util(T), cardinality = (T:2)>
[22.5 20. ]
----
optimal policy for D:
<Potential util(S,T), cardinality = (S:3,T:2)>
[[0 0]
 [0 0]
 [1 0]]
<Potential util(S,T,D), cardinality = (S:3,T:2,D:2)>
[[[ 87.5          0.        ]
  [ 20.           0.        ]]

 [[ 32.85714286   0.        ]
  [ 20.           0.        ]]

 [[-30.48780488   0.        ]
  [ 20.           0.        ]]]
----
```