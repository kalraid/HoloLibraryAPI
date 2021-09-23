# Decorator
def constant(func):
    def func_set(self, value):
        raise TypeError

    def func_get(self):
        return func()
    return property(func_get, func_set)

# const class
class _Const(object):
    @constant
    def PAGE_INDEX(self):
        return "/index"

    @constant
    def PAGE_MEMBER_LOGIN(self):
        return "/member/login"

    @constant
    def PAGE_MEMBER_LOGOUT(self):
        return "/member/logout"

CONST = _Const()

print(CONST.PAGE_INDEX) # /index
print(CONST.PAGE_MEMBER_LOGIN) # /member/login
print(CONST.PAGE_MEMBER_LOGOUT) # /member/logout

CONST.PAGE_MEMBER_LOGIN = "another_page" # TypeError