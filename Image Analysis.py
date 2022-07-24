def obfuscated(password):
    obfuscated_password = password[0] + '#'*(len(password)-2) + password[len(password)-1]
    return obfuscated_password
#I could have made the code smaller by writing these details inside the last print, but I wanted to use a function for this part

name = input('Please enter your name:\n')
password = input('Please enter a password:\n')

print('Welcome', name)
print('Your password has', len(password), 'letters')

if len(password) < 8:
    print('Your password has less than 8 characters. We recommend at least 8 characters for the safety of your account.')

x = obfuscated(password)

print('This is the obfuscated version of your password:', x)