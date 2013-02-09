from pie.main import entry_point

__author__ = 'sery0ga'

#from rpython.jit.codewriter.policy import JitPolicy

def target(driver, args):
    driver.exe_name = 'pie'
    return entry_point, None

def jitpolicy(driver):
    from rpython.jit.codewriter.policy import JitPolicy
    return JitPolicy()
