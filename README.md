```_**expression-evaluator_**``
```	
test data:
e = expression()
v, rc = e.interpret('123.22*234*2.3-23')
e.set_visitor(structure_visitor())
e.visit()
e.set_visitor(value_visitor())
e.visit()


n = number()
v, rc = n.interpret('383.220')
n.set_visitor(structure_visitor())
n.visit()
n.set_visitor(value_visitor())
n.visit()


t = term()
v, rc = t.interpret('23*34*56')
t.set_visitor(structure_visitor())
t.visit()
t.set_visitor(value_visitor())
t.visit()


e = expression()
v, rc = e.interpret('-123.22*234*2.3-23')
e.set_visitor(structure_visitor())
e.visit()
e.set_visitor(value_visitor())
e.visit()


e = expression()
v, rc = e.interpret('-123.22*234*2.3-23+4*5-6*7*8/2*3-7')
e.set_visitor(structure_visitor())
e.visit()


e = expression()
v, rc = e.interpret('-123.22*234*2.3-23+4*5-6*7*8/2*3-7')
e.set_visitor(value_visitor())
e.visit()