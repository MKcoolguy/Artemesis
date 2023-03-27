AuthenticatedUsers = open("Users.txt", "a")
userName = input('What is the username the user would like to use?\n')
passWord = input('WHat is the password the user would like to use?\n')

AuthenticatedUsers.writelines(userName)
AuthenticatedUsers.writelines(passWord)