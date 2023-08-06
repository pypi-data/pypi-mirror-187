## About this package

This package is available on https://pypi.org/project/brdocvalidator/ , you can easily validate brazilians documents like CPF and CNPJ. Also some functions to help validate email, birth date, and new functionalities will appear soo

Code on github
https://github.com/rafaelscone/brdocvalidator

## How to use

```bash
pip3 install brdocvalidator
```

In your python file
```py
import brdocvalidator

cpf = '111.111.111-11'
cnpj = '11.111.111/1111-11'
birthDay = "26/07/2010"
my_password ='JtR55$$_'
my_email = "email@email.com"

# return date format %d-%m-%Y or False
print(brdocvalidator.check_birth_date(birthDay))

# Return just CPF number or False
# check_doc check CPF or CNPJ
print(brdocvalidator.check_doc(cpf))
print(brdocvalidator.check_cpf(cpf))

# Return just CNPJ number or False
print(brdocvalidator.check_doc(cnpj))
print(brdocvalidator.check_cnpj(cnpj))

# Encode your password
encoded_password= brdocvalidator.encodePass(my_password)
print(encoded_password)

# Check if password match
test = brdocvalidator.comparePass(encoded_password,my_password)
print("Result pass:", test)

# Check email 
myemail =  brdocvalidator.check_email(my_email)
print(myemail)
```

### Feel free to send me news, bugs and suggestions to this package
Rafael Schneider - rafaelscone


