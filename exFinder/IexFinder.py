# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 08:42:17 2021

@author: zoufine Lauer Bare
"""

import sympy as sym
import numpy as np
import ipywidgets as widgets
import pandas as pd
import plotly.graph_objects as go
from sympy import sqrt, sin, cos, tan, exp, log, ln

x, y, z = sym.symbols('x y z', real=True)


class statPoint:
    def __init__(self, point, eigenvalues):
        self.point=point
        self.eigenvalues=eigenvalues
        if (np.array(list(eigenvalues))>0).all():
            self.eType='Minimum'
        elif  (np.array(list(eigenvalues))<0).all():
            self.eType='Maximum'
        elif  np.array(list(eigenvalues)).prod()==0:
            self.eType='Not Classifiable'        
        else:
            self.eType='Saddle Point'
  


class Xtreme():
    
    def __init__(self):
        
        self.f = widgets.Text(
            value='x**2*(x + 1) + y**2*(x - 1)',
            description=r'$f(x, y)=$',
            disabled=False
            )

        trace = go.Table(
            header=dict(values=['Stationary points', 'Eigenvalues and algebraic multiplicity', 'Type'],
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
            cells=dict(values=[[],
                               [],
                              []],
                       line = dict(color='#7D7F80'),
                       fill = dict(color='#EDFAFF'),
                       align = ['left'] * 5))

        #layout = dict(width=500, height=300)
        data = [trace]
        self.fig = go.FigureWidget(data=data)#, layout=layout)  
        
        lF = sym.latex(eval(self.f.value))
        lH = sym.latex(self.H(self.f))
        
        self.fig.update_layout(
            title=r"$f(x, y) = %s\text{, }H_f(x, y)=%s$ " %(lF, lH))
        

    def H(self, f):
        """


        Parameters
        ----------
        f : symbolic function

        Returns
        -------
        Hf : Hessian matrix

        """
        
        f = eval(self.f.value)
        
        Hf=sym.Matrix(([sym.diff(f,x,x),sym.diff(f,x,y)],[sym.diff(f,x,y),sym.diff(f,y,y)]))
        return Hf

    def exFinder(self, f):
        """


        Parameters
        ----------
        f : symbolic function from R^2 to R

        Returns
        -------
        statPoints : stationary points
        H : Hessian at those points

        """
        

        
        system=[sym.diff(f,x),
                sym.diff(f,y),
               ]


        solSet=sym.nonlinsolve(system,[x,y])

        solSetReal=[]
        for i in list(solSet):
            if i[0].is_real and i[1].is_real:
                solSetReal.append(i)
            elif abs(sym.im(i[0]).evalf()) < 10**(-120) and abs(sym.im(i[1]).evalf()) < 10**(-120):
                solSetReal.append((sym.re(i[0]).evalf(), sym.re(i[1]).evalf()))

        statPoints=[]
        for i in solSetReal:
            H=sym.Matrix(([sym.diff(f,x,x),sym.diff(f,x,y)],
                          [sym.diff(f,x,y),sym.diff(f,y,y)]))
            H=H.subs(x,i[0])
            H=H.subs(y,i[1])
            statPoints.append(statPoint(i,H.eigenvals()))
                
 
        
        points = []
        eigenvalues = []
        eType = []
        
        for i in statPoints:
            #print(i.point, i.eigenvalues, i.eType)
             points.append('(%s, %s)' %(i.point[0], i.point[1]))
             #points.append('%s' % i.point)
             eigenvalues.append('%s' % i.eigenvalues)   
             eType.append('%s' % i.eType)
          
        


        table = self.fig.data[0]
        table.cells.values = [points,
                              eigenvalues,
                              eType
                             ]
        
        self.fig.update_layout(
                             title=r"$f(x, y) = %s\text{, }H_f(x, y)=%s$ " %(sym.latex(f), sym.latex(self.H(self.f))))
         

        return points, eigenvalues, eType
    
    def on_button_clicked(self, b):
        self.exFinder(eval(self.f.value))
        return 
    
    def compute(self):
        button = widgets.Button(description="Update")
        button.on_click(self.on_button_clicked)
        display(self.f, button, self.fig)
        return
