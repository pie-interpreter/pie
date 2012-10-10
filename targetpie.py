__author__ = 'sery0ga'

from pie.main import entry_point
from pypy.jit.codewriter.policy import JitPolicy

def target(driver, args):
    driver.exe_name = 'pie'
    return entry_point, None

def jitpolicy(driver):
    return JitPolicy()
