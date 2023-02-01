
# shell.fuelreplenishment
Modelo de calculo de productos
# inputs

Calculo de productos para envio de combustible

Inputs:
Flujo de venta de combustible:
m0, m1, m2, m3 flujs de ventas en litros por minuto [l/min]. m0 corresponde a v-power diesel, m1 a evolux, m2 a v-power nafta y m3 a nafta super.

Caracteristivcas del camion:
C capacidad de un tanque cisterna, para la estacion 1132 es de 25000
c_min capacidad de los compartientos

Stocks:
q0,q1,q2,q3 suma de stocks correspondientes,  q0 corresponde a v-power diesel, q1 a evolux, q2 a v-power nafta y q3 a nafta super.

Capacidades maximas de almacenamiento de productos de la estacion
c0_max, c1_max,c2_max, c3_max son las camapcidades maximas de almacenamiento de productos de la estacion. c0_max corresponde a v-power diesel, c1_max a evolux, c2_max a v-power nafta y c3_max a nafta super.


fecha de revision, es la hora en la cual fueron tomados los stocks, debe estar perfectamente sincronizada con los datos de stock, sino se generan errores que pueden ser importantes

#Matematica

Resumen de la matematica para el calculo de productos

[Edited with overleaft](Shell_doc_calc.pdf)
