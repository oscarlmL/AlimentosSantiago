from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(plato, carro):
    keys = carro.keys()
    for id_plato in keys:
        if int(id_plato) == plato.id_plato:
            return True
    return False;

@register.filter(name='carro_quantity')
def carro_quantity(plato, carro ):
    keys = carro.keys()
    keys = carro.keys()
    for id_plato in keys:
        if int(id_plato) == plato.id_plato:
            return carro.get(id_plato)
    return 0;

@register.filter(name='precio_total')
def precio_total(plato, carro ):
    return plato.valor_plato * carro_quantity(plato, carro)


@register.filter(name='precio_total_carro')
def precio_total_carro(plato, carro):
    sum = 0 ;
    for p in plato:
        sum += precio_total(p, carro)

    return sum

#mis pedidos
@register.filter(name='multiplicar')
def multiplicar(num, num1):
    return num*num1
