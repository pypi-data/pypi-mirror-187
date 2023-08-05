from . import dirs
from . import fechas

from .cl_ReporteBase import *

__all__ = ['DTE',]

class DTE(ReporteBase):

    def __init__(
        self,
        fecha_i = fechas.hoy(),
        fecha_f = fechas.hoy(),
        periodo=None,
        filtro = 'ultimos',
        parques = [],
        tabla_datos = 'Q_RepItems',
        col_filtro = 'NEMO',
        dir_salida = dirs.raiz,
        ):

        dir_descarga, dir_extraccion = self.__elegir_dirs(filtro=None)

        super().__init__(
            fecha_i = fecha_i,
            fecha_f = fecha_f,
            periodo=periodo,
            nemo_rpt = 'DTE_UNIF',
            nombre = 'DTE',
            formato_nombre_archivo = 'DTE%y%m',
            parques = parques,
            extension = 'mdb',
            tabla_datos = tabla_datos,
            tabla_fecha = 'VALORES_PERIODO',
            col_filtro = col_filtro,
            dir_salida = dir_salida,
            dir_descarga = dir_descarga,
            dir_extraccion = dir_extraccion,
            funcion_archivos_necesarios = fechas.iterar_mensual,
            valores_custom_filtro= {'finales':self.__filtrar_dtes_finales}
            )
        
        self.filtro = filtro
        
    #--------------------------
    #
    #Fin de la función __init__
    #
    #--------------------------
    def __filtrar_dtes_finales(self,df):
        #Toma un dataframe resultante de la funcion cl_ApiCammesa.ApiCammesa.consultar()
        flt = df['titulo'].str.upper().str.startswith('DTE EMISIÓN 08/')
        return df[~flt]
    
    def __get_dirs(self,funcion):
        try:
            dir_descarga = funcion() + '\\00 ZIP'
        except: 
            dir_descarga = dirs.raiz + '\\00 ZIP'

        try:
            dir_extraccion = funcion() + '\\01 MDB'
        except:
            dir_extraccion = dirs.raiz + '\\01 MDB'
            
        return dir_descarga, dir_extraccion
    
    def __elegir_dirs(self,filtro=None):
        
        if filtro is None or filtro =='ultimos':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dte)
                    
        elif filtro == 'iniciales':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dtei)
                    
        elif filtro == 'finales':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dtef)
        else:
            dir_descarga    = dirs.raiz + '\\00 ZIP'
            dir_extraccion  = dirs.raiz + '\\01 MDB'
            
        return  dir_descarga, dir_extraccion
    
    @property
    def filtro(self):
        return self._filtro
    
    @filtro.setter
    def filtro(self,val):
        if val != False:
            self._filtro = self.check_filtro(val)
            self.dir_descarga, self.dir_extraccion = self.__elegir_dirs(self.filtro)
            self._actualizar_archivos()

    # Agregado de funcionalidades a funciones de la clase superior
    def consultar(self,exportar_consulta=False,dir_consulta=None,filtro=None):
        
        if filtro is not None:
            self.filtro = filtro
        
        super().consultar(
            exportar_consulta=exportar_consulta,
            dir_consulta=dir_consulta,
            filtro=self.filtro
            ) 
    
    def descargar(self,exportar_consulta=False,dir_consulta=None,filtro=None):
        
        if filtro is not None:
            self.filtro = filtro
        
        super().descargar(
            exportar_consulta=exportar_consulta,
            dir_consulta=dir_consulta,
            filtro=self.filtro
            ) 
        
    def cargar(self,descargar=False,filtro=None,exportar_consulta=False):
        
        if filtro is not None:
            self.filtro = filtro
        
        super().cargar(
            descargar=descargar,
            filtro=self.filtro,
            exportar_consulta=exportar_consulta
            )
    
    def a_excel(self,descargar=False,filtro=None,exportar_consulta=False):
        
        if filtro is not None:
            self.filtro = filtro
        
        super().a_excel(
            descargar=descargar,
            filtro=self.filtro,
            exportar_consulta=exportar_consulta
            )