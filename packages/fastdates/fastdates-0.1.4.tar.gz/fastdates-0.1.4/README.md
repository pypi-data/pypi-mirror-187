# fastdates

## What is it?
fastdates module allows users to get dates using a declarative language in the form of simple, human-readable Python methods. 

## Examples

```python
from fastdates import Fastdates

fd = Fastdates.DateGenerator()

fd.get_next_n_days(5)
['2022-10-26', '2022-10-27', '2022-10-28', '2022-10-29', '2022-10-30']
fd.get_last_day_of_previous_month()
'2022-09-30'
fd.get_previous_n_months(3)
['2022-09', '2022-08', '2022-07']
```