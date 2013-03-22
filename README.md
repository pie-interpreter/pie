# Pie - PHP interpreter
Pie is a [PHP](http://php.net) interpreter which is being created to be faster and more comfortable to use than current one.

We don't try to make Pie 100% compatible. We respect a devotion of PHP core developers to backward compatibility. We think that the language simplicity and consistency suffer from current too strong orientation on backward compatibility. Pie won't support PHP language features which are universally recognized bad practices or too illogical and make language understanding harder. At the same time, we know how important most of current functionality are. If you develop with some appropriate limitations in mind, you won't have any difficulties with moving on Pie.

Pie is all about speed. We believe that a big number of modules and settings, increasing PHP performance in production, complicate language understanding and its usage. We aspire after you start thinking about the speed of your projects later than you do now and such extensions as APC will disappear as class.

## Analogues
We were inspired by [HippyVM](https://bitbucket.org/fijal/hippyvm) project which is in active development right now too.

## Installation notes
We don't provide executable packages for now. You need to compile the code yourself if you want to try it.

Step by step installation:

1. Download [pypy sources](https://bitbucket.org/pypy/pypy)
2. Download [pypy executable](http://pypy.org/download.html#default-with-a-jit-compiler). Use [these notes](http://pypy.org/download.html#installing) to install
3. Download Pie sources
4. Run ./compile.sh
5. Find Pie executable in pie/ directory

## Additional info
Visit our [blog](http://pie-interpreter.blogspot.com/ "Pie blog")