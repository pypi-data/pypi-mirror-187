
## Installation

Install the Package using the command -

```bash
   $ pip install topsis-nandini
```
    
```bash
    >>> import topsis-nandini as tp
    >>>df= [
       ['MobilePhone','RAM','Memory','DisplaySize','Battery']
        ['A',16,12,250,5]
        ['B',16,8,200,3]
        ['C',32,16,300,4]
        ['D',32,8,275,4]
        ['E',16,16,225,2]
        ]
    >>> w="1,1,1,1"
    >>> i="+,+,+,+"
    >>> tp.topsis(df,w,i)
```
You may use the Package via commandline as
```bash
   $ python [package name] [path of csv as string] [list of weights as string] [list of sign as string] [output csv filename as string]
```