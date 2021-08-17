# -*- coding: utf-8 -*-

"""
Created on May 7, 2018
This is an improvment on the original program posted here:
https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/

The original program tightly coupled GUI dependencies into the Controller class, which defeats the whole MVC paradgim.

The example below is an improvement on the original program.
Each of the Model, View, Controller and SidePanel objects are in their own modules.
The program now runs on Python 2 & Python3, without any modifications.
"""

from controller import Controller

if __name__ == '__main__':
    c = Controller()
    c.run()
