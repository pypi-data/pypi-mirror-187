INDICADORES DE BOT GUS


supertrend(df,atr_periodsuper,factorsuper)
Devuelve 1: señal de compra o venta

bandas_bollinger(datos, periodo, desviaciones)
Devuelve 3 valores: valor banda superior, valor banda inferior, valor media movil

estocastico(df,k_period,d_period)
Devuelve 2 valores: Valor estocastico K y estocastico D

macd(df,rapidaema,lentoema,senialperiodo)
Devuelve 3 valores: Valor Macd, Valor señal de macd, valor divergencia

rsi(df,rsi_period,ema,longirsi,emamovil)
Devuelve 2 valores: Valor de rsi y valor de media movil de rsi

tendenciaactual(df,cualma,ma1,ma2,ma3)
Devuelve 1: Valor de tendencia actual

soportesyresistencias(df,tipo)
Devuelve 5 valores: Pivote central, soporte 1, resistencia 1, soporte 2, resistencia 2

squeeze_momentum(df,length, mult, length_KC, mult_KC):
Devuelve 1: Valor de compra o venta

dmi(df,period,perioddi)
Devuelve 3: Valores adx, adx + , adx -

aroon(df,periodoaron)
Devuelve 2: Valores Arron arriba, Arron Abajo

chandelierexit(df, atr_period, atrmulti)
Devuelve 1: Valor de compra o venta

rvi(df, longitud)
Devuelve 2: Valores rvi y rvi señal

williamd(df,periodo)
Devuelve 1: Valor william %D

keltnerchannel(df,cual, longitud, multipl, atrlongi)
Devuelve 3: Valores banda superior, banda inferior, media movil

coppockcurve(df, roclargo, roccorto,wma):
Devuelve 1: Valor curva coppock

ao(df, corto,largo)
Devuelve 1: Valor oscilador asombroso


