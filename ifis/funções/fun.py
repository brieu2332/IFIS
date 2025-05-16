#espiral fechado
def campo_rotacional(x, y):
    return (-y, x)

#para o centro porem se deixar - somente em x ou y, interessante
def campo_atrator(x, y):
    modulo = math.hypot(x, y)
    if modulo == 0:
        return (0, 0)
    return (-x / modulo, -y / modulo)

#sai da tela
def campo_repulsor(x, y):
    modulo = math.hypot(x, y)
    if modulo == 0:
        return (0, 0)
    return (x / modulo, y / modulo)

#muitos minis espirais
def campo_senoidal(x, y):
    return (math.sin(y / 20), math.cos(x / 20))


#espiral aberto
def campo_espiralado(x, y):
    return (-y + x, x + y)


#aponta para o centro
def campo_linear(x, y):
    return (-x, -0.5 * y)

#avenida
def campo_eder(x, y):
    u = x + y
    v = x - y
    m = math.sqrt(u*u + v*v)
    if m == 0:
        m = 1
    return (u/m, v/m)
