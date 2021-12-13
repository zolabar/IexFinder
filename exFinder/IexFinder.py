# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 08:42:17 2021

@author: zoufine Lauer Bare
v1.0.2
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
            header=dict(values=['<b>Stationary points</b>', 
                                '<b>Eigenvalues and algebraic multiplicity</b>', 
                                '<b>Type</b>',
                                 '<b>Value</b>'],
                        #line = dict(color='#7D7F80'),
                        #fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
            cells=dict(values=[[],
                               [],
                              [],
                              []],
                       #line = dict(color='#7D7F80'),
                       #fill = dict(color='#EDFAFF'),
                       align = ['left'] * 5))

        #layout = dict(width=500, height=300)
        data = [trace]
        self.fig = go.FigureWidget(data=data)#, layout=layout)  
        

                
        
        f_num = sym.lambdify((x,y), eval(self.f.value))
        
        x_ = np.linspace(-5, 5, 100) 
        y_ = np.linspace(-5, 5, 100)
        
        X, Y = np.meshgrid(x_, y_)
        
        self.fig2 = go.FigureWidget(data=go.Surface(
            x=x_,
            y=y_,
            z=f_num(X, Y),
            colorscale='Rainbow'))
        
        self.fig2.update_traces(contours_z=dict(show=True, usecolormap=True,
                                   project_z=True))
        
        self.fig2.add_trace(go.Scatter3d(x=[-2/3, 0], y=[0, 0], z=[0.15, 0],
                                   mode='markers',
                                            marker=dict(
                                                    size=5,
                                                    color='black',                # set color to an array/list of desired values
                                                    opacity=0.8
                                                )))
        
        lF = sym.latex(eval(self.f.value))
        lH = sym.latex(self.H(self.f))
        
        self.fig.update_layout(
            title=r"$H_f(x, y)=%s$ " %(lH))
 
        self.fig2.update_layout(
            title=r"$f(x, y) = %s$ " %(lF))  
        
        self.html = widgets.HTMLMath(
                value=r"$\begin{matrix}\frac{\partial}{\partial x}%s=0\\\frac{\partial}{\partial y}%s=0\end{matrix}$"%(sym.latex(sym.diff(eval(self.f.value), x)), sym.latex(sym.diff(eval(self.f.value), y))),
                #description=r'Gradien$',
            )
        
        self.html2 = widgets.HTMLMath(
                value=r"$%s$"%(lH),
                #description=r'Gradien$',
            )        

        #self.fig2.update_layout(template = 'plotly_dark')
        #self.fig2.update_layout(template = 'ggplot2')
        self.fig2.update_layout(template = 'simple_white')
        
        
        
        self.colormap = widgets.Dropdown(
                    options=['Rainbow', 
                             'Hot',
                             'Plotly3',
                             'RdBu',
                             'PuRd',
                             'Purples',
                             'Greys',
                             'Bluered',
                             'Thermal',
                             'Viridis',
                             'amp',
                             'Sunset'],
                    value='Rainbow',
                    # rows=10,
                    description='Colormap',
                    disabled=False
                )

        self.exFinder(eval(self.f.value))


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
        

        
        system = [sym.diff(f, x),
                  sym.diff(f, y),
                 ]


        solSet=sym.nonlinsolve(system, [x, y])

        solSetReal=[]
        for i in list(solSet):
            if i[0].is_real and i[1].is_real:
                solSetReal.append(i)
            elif abs(sym.im(i[0]).evalf()) < 10**(-120)  and abs(sym.im(i[1]).evalf()) < 10**(-120):
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
        
        values = []
        
        x_array = []
        y_array = []
        
        fNum = sym.lambdify((x,y), f)
        
        for i in statPoints:
            #print(i.point, i.eigenvalues, i.eType)
             points.append('(%s, %s)' %(i.point[0], i.point[1]))
             x_array.append(i.point[0])
             y_array.append(i.point[1])
             #points.append('%s' % i.point)
             eigenvalues.append('%s' % i.eigenvalues)   
             eType.append('%s' % i.eType)
             wert = round(fNum(float(i.point[0]), float(i.point[1])), 2)
             values.append(wert)
          
        array = np.asfarray(x_array+y_array)+0.0001
 
        limit = 2*abs(array).max()
        
        limit = max(limit, 2.5)
        

        table = self.fig.data[0]
        table.cells.values = [points,
                              eigenvalues,
                              eType,
                              values
                             ]
        
        x_ = np.linspace(-limit, limit, 100) 
        y_ = np.linspace(-limit, limit, 100)
        
        X, Y = np.meshgrid(x_, y_)
        
 
        
        f_num = sym.lambdify((x, y), eval(self.f.value))

        self.fig2.data[0].x = x_
        self.fig2.data[0].y = y_
        self.fig2.data[0].z = f_num(X, Y)
        
        
        
        self.fig2.data[1].x = x_array
        self.fig2.data[1].y = y_array
        self.fig2.data[1].z = values        
        
        
        self.fig.update_layout(
            title="Stationary points and characterization"                 
            )

        self.fig2.update_layout(
                             title=r"$f(x, y) = %s$ " %(sym.latex(f)))   
        

        
        
        self.html.value = r"$\begin{matrix}%s=0\\%s=0\end{matrix}$"%(sym.latex(sym.diff(f, x)), sym.latex(sym.diff(f, y)))
        
        self.html2.value = r"$H_f(x, y)=%s$"%(sym.latex(self.H(self.f)))
        

        return points, eigenvalues, eType
    
    def on_button_clicked(self, b):
        self.exFinder(eval(self.f.value))
        return 
    
    def update_colorscale(self, change):
        self.fig2.data[0].colorscale = self.colormap.value
        return     
    
    def compute(self):
        button = widgets.Button(description="Update")
        button.on_click(self.on_button_clicked)     
        self.colormap.observe(self.update_colorscale, names='value')
        #display(self.f, button, self.colormap, self.fig, self.fig2)
        
        container = widgets.HBox([self.f, button, self.colormap,
                                  ])
        container2 = widgets.HBox([button, 
                                  ])        
        
        container3 = widgets.HBox([
                                  self.fig, self.fig2
                                  ])  
 
        text0 = widgets.HTML(
            value="<b>Step by step &#128512</b>",
            #placeholder='Some HTML',
            #description='Some HTML',
        )        
        
        
        html0 = widgets.HTMLMath(
                value=r"$\begin{matrix}\frac{\partial f}{\partial x}=0\\\frac{\partial f}{\partial y}=0\end{matrix}$",
                #description=r'Gradien$',
            )        
        
        
        text = widgets.HTML(
            value="Setting the gradient of <i>f</i> to zero, gives the following system of equation in <i>x</i> and <i>y</i>. Solving it yields the <b>stationary points</b>.",
            #placeholder='Some HTML',
            #description='Some HTML',
        )
        
        text1 = widgets.HTML(
            value="    yields       ",
            #placeholder='Some HTML',
            #description='Some HTML',
        )        
        
        text2 = widgets.HTML(
            value="Then, put the stationary points into the following <b>Hessian</b> and compute its eigenvalues.",
            #placeholder='Some HTML',
            #description='Some HTML',
        )        

        container3_5 = widgets.HBox([text0])         

        container4 = widgets.HBox([text])         
        
        container5 = widgets.HBox([html0, text1, self.html])   
        
        container6 = widgets.HBox([text2])         
        
        container7 = widgets.HBox([self.html2])          

        display(widgets.VBox([container, 
                              #container2,
                              container3,
                              container3_5,
                              container4,
                              container5,
                              container6,
                              container7,
                              ]))
        
        return
