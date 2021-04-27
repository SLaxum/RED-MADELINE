import random as rn
import numpy as np
import pandas as pd
import os
from Layers import *

class Config:

    #CONSTRUCTOR
    def __init__(self):
        self.Entradas = []
        self.Salidas = []
        self.Entranamiento = ''
        self.capas = []
    
    #METODO PARA GENERAR PESOS
    def Generar_pesos(self, row, col):
        Matriz = []
        for N in range(row):
            Fila = []
            for M in range(col):
                Fila.append(round(rn.uniform(-1, 1), 2))
            Matriz.append(Fila)
        return Matriz

    #METODO PARA GENERAR UMBRALES
    def Generar_Umbrales(self, row):
        Fila = []
        for N in range(row):
            Fila.append(round(rn.uniform(-1, 1), 2))
        return Fila

    # LLENAR MATRICES ENTRADAS Y SALIDAS
    def NormalizarDatos(self, ruta):
        Matriz = pd.read_csv(ruta, delimiter=' ')
        col = Matriz.columns
        column = Matriz.to_numpy()
        self.Entranamiento = os.path.basename(os.path.splitext(ruta)[0])

        for i in range(len(col)):
            if 'X' in col[i]:
                Fila = []
                for j in range(len(column)):
                    Fila.append(column[j,i])
                self.Entradas.append(Fila)
            else:
                Fila = []
                for j in range(len(column)):
                    Fila.append(column[j,i])
                self.Salidas.append(Fila)

    # AGREGAR CAPAS OCULTAS
    def AgregarCapas(self, capa, neuronas, funcActivacion):
        encabezado = ['Capa', 'Neuronas', 'Func Activacion']
        self.capas.append([capa, neuronas, funcActivacion])
        
        return pd.DataFrame(data=self.capas, columns=encabezado)

    # INICIAR ENTRENAMIENTO
    def Entrenar(self, rataAprendizaje, errorLineal, numeroIteraciones, funcionSalida):

        layers = Layers()
        self.Entradas = np.array(self.Entradas)
        self.Salidas = self.NormalizarSalidas(self.Salidas) if len(self.Salidas)==1 else (self.Salidas)
        EntradasCapas = []
        _EntradasCapas = []

        for I in range(len(self.capas)):

            # CONDICION PARA ENTRADA Y CAPA 1
            if(I == 0):
                pesos = self.Generar_pesos(len(self.Entradas), self.capas[I][1])
                umblrales = self.Generar_Umbrales(self.capas[I][1])

                print('ENTRADAS x CAPA:', I, '=', len(self.Entradas), 'x', self.capas[I][1])
                print()

                for J in range(len(self.Entradas[0])):

                    entrada = self.Entradas[:,J]

                    func = layers._FuncionActivacion(self.capas[I][2])
                    EntradasCapas.append(layers.FuncionActivacionCapas(func, layers.FuncionSoma(entrada, pesos, umblrales)))

                print(np.array(EntradasCapas))
                print()
                print()
                
             # CONDICION PARA CAPAS INTERMEDIAS
            if(I > 0 & I < (len(self.capas) - 1)):
                pesos = self.Generar_pesos(self.capas[I-1][1], self.capas[I][1])
                umblrales = self.Generar_Umbrales(self.capas[I][1])

                print('CAPA', I-1, 'x CAPA:', I, '=', self.capas[I-1][1], 'x', self.capas[I][1])
                print()

                for J in range(len(EntradasCapas)):

                    if( J == 0 ):
                        _EntradasCapas = EntradasCapas
                        EntradasCapas = []

                    entradasCapas = _EntradasCapas[J][:]

                    func = layers._FuncionActivacion(self.capas[I][2])
                    EntradasCapas.append(layers.FuncionActivacionCapas(func, layers.FuncionSoma(entradasCapas, pesos, umblrales)))

                print(np.array(EntradasCapas))
                print()
                print()
                
            # CONDICION PARA LA ULTIMA CAPA Y SALIDAS
            if(I >= (len(self.capas) - 1)):
                pesos = self.Generar_pesos(self.capas[I][1], len(self.Salidas[0]))
                umblrales = self.Generar_Umbrales(len(self.Salidas[0]))

                print('CAPA', I, 'x ENTRADAS', '=', self.capas[I][1], 'x', len(self.Salidas[0]))
                print()

                for J in range(len(EntradasCapas)):

                    if( J == 0 ):
                        _EntradasCapas = EntradasCapas
                        EntradasCapas = []

                    entradasCapas = _EntradasCapas[J][:]

                    func = layers._FuncionActivacion(funcionSalida)
                    salida = self.Salidas[J][:]
                    print(layers.ErrorPatron(
                        layers.ErrorLineal(salida, 
                        layers.FuncionActivacionSalidas(func, 
                        layers.FuncionSoma(entradasCapas, pesos, umblrales))), len(self.Salidas[0])))
                
        print()
        print()
        print('//////////// - FIN ENTRENAMIENTO - ////////////')
        print()

    # LIMPIAR CAPAS
    def Limpiar(self):
        self.capas = []

    def NormalizarSalidas(self, salida):
        salidas = []
        for i in range(len(salida[0])):
            s = []
            for j in range(len(salida)):
                s.append(salida[j][i])
            salidas.append(s)
        return salidas

if __name__ == '__main__':
    print("Hola") 