# promulgate

Simple single threaded event library. Inspired by this[https://stackoverflow.com/a/2022629] stackoverflow answer. 

## Example 

```python
from dataclasses import dataclass
from promulgate import Promulgation

@dataclass
class RegisterUserPromulgation(Promulgation)
    email: str
    password: str


def handle_register_user(prmlg : RegisterUserPromulgation) -> None:
    print(f"New user with email {prmlg.email} and password ***")


RegisterUserPromulgation.subscribe(handle_register_user)

event = RegisterUserPromulgation("test@test.com", "super.1.secret!")
event.promulgate()

# New user with email test@test.com and password *** 
```